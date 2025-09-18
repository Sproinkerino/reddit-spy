import os
import asyncpraw
import requests
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn

# --- 1. SETUP: LOAD CREDENTIALS FROM .ENV FILE ---
# This securely loads your keys without hardcoding them in the script.
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if all credentials are provided
if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, OPENAI_API_KEY]):
    raise ValueError("Missing credentials in the .env file. Please ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, and OPENAI_API_KEY are set.")

# Authenticate with the OpenAI API
# Note: For newer versions of openai package, we don't set the global api_key
# Instead, we pass it directly to the client

# --- FASTAPI APP SETUP ---
app = FastAPI(title="Reddit Stalker API", description="API for analyzing Reddit user data")

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://localhost:3001",  # Alternative React port
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://127.0.0.1:3001",  # Alternative localhost
        "https://your-frontend-domain.com",  # Replace with your actual frontend domain
        "*"  # Allow all origins for development (remove in production)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Request model for the API
class AnalyzeUserRequest(BaseModel):
    user_id: str
    user_to_search: str
    parameters: Dict[str, Any]

# Response model for the API
class AnalyzeUserResponse(BaseModel):
    success: bool
    user_id: str
    analyzed_user: str
    summary: Optional[str] = None
    error: Optional[str] = None


# --- 2. FUNCTION TO FETCH REDDIT DATA (ASYNC) ---
async def get_reddit_user_data(username, parameters: Dict[str, Any]):
    """
    Fetches recent submissions and comments for a given Reddit username.
    Parameters can include post_limit and comment_limit.
    """
    post_limit = parameters.get("post_limit", 10)
    comment_limit = parameters.get("comment_limit", 100)
    
    try:
        # Initialize AsyncPRAW with your credentials
        reddit = asyncpraw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )

        redditor = await reddit.redditor(username)

        # Use a list to store all the text content
        content = []

        # Fetch recent submissions (posts)
        async for submission in redditor.submissions.new(limit=post_limit):
            # Add post title and selftext (if it exists)
            content.append(f"Post Title: {submission.title}")
            if submission.selftext:
                content.append(f"Post Body: {submission.selftext}")

        # Fetch recent comments
        async for comment in redditor.comments.new(limit=comment_limit):
            content.append(f"Comment: {comment.body}")

        if not content:
            raise ValueError(f"No recent public activity found for u/{username}")

        # Close the reddit instance
        await reddit.close()

        # Join all collected text into a single string, separated by newlines
        return "\n---\n".join(content)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching data from Reddit: {str(e)}")


# --- 3. FUNCTION TO SUMMARIZE TEXT WITH LLM ---
def summarize_with_llm(user_data, username, parameters: Dict[str, Any]):
    """
    Sends the user's data to an LLM and returns a summary.
    Parameters can include model, temperature, and custom prompts.
    """
    model = parameters.get("model", "gpt-4o")
    temperature = parameters.get("temperature", 0.5)
    custom_prompt = parameters.get("custom_prompt")

    # This is your "prompt engineering" part. Be specific!
    system_prompt = "You are a helpful assistant that analyzes Reddit user histories to create a concise, insightful summary. Be objective and base your analysis strictly on the provided text."

    if custom_prompt:
        user_prompt = custom_prompt.format(username=username, user_data=user_data)
    else:
        user_prompt = f"""
        Please analyze the following collection of recent Reddit posts and comments from the user u/{username}.
        Based *only* on this data, generate a summary that covers:
        1.  **Main Interests:** What are the recurring topics, hobbies, or communities they engage with?
        2.  **Overall Tone:** Do they seem helpful, argumentative, humorous, or technical?
        3.  **Activity Pattern:** What kind of content do they typically post or comment on?

        Keep the summary to about 3-4 paragraphs.

        --- USER DATA ---
        {user_data}
        --- END USER DATA ---
        """

    try:
        # Use direct HTTP requests to avoid package conflicts
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": 1000
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            summary = result['choices'][0]['message']['content']
            return summary
        else:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {response.status_code} - {response.text}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with OpenAI API: {str(e)}")


# --- 4. API ENDPOINTS ---
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Reddit Stalker API is running", "status": "healthy"}

@app.post("/analyze", response_model=AnalyzeUserResponse)
async def analyze_user(request: AnalyzeUserRequest):
    """
    Analyze a Reddit user based on their public posts and comments.
    
    Args:
        request: Contains user_id (caller), user_to_search (target), and parameters (configuration)
    
    Returns:
        AnalyzeUserResponse with analysis summary or error information
    """
    try:
        # Step 1: Get the data from Reddit (now async)
        reddit_data = await get_reddit_user_data(request.user_to_search, request.parameters)
        
        # Step 2: Send it for summarization
        llm_summary = summarize_with_llm(reddit_data, request.user_to_search, request.parameters)
        
        # Step 3: Return the successful response
        return AnalyzeUserResponse(
            success=True,
            user_id=request.user_id,
            analyzed_user=request.user_to_search,
            summary=llm_summary
        )
        
    except HTTPException:
        # Re-raise HTTPExceptions as they already have proper status codes
        raise
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# --- 5. SERVER STARTUP ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )