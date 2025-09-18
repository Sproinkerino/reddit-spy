"""
Test OpenAI API functionality separately
"""

import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def test_openai_basic():
    """Test basic OpenAI API connection"""
    print("Testing OpenAI API connection...")
    print(f"API Key present: {'Yes' if OPENAI_API_KEY else 'No'}")
    print(f"API Key starts with: {OPENAI_API_KEY[:10] if OPENAI_API_KEY else 'None'}...")
    
    if not OPENAI_API_KEY:
        print("ERROR: No OpenAI API key found in .env file")
        return False
    
    try:
        # Test with a simple completion
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello, OpenAI API is working!'"}
            ],
            max_tokens=50,
            api_key=OPENAI_API_KEY
        )
        
        result = response.choices[0].message.content
        print(f"SUCCESS: {result}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_openai_with_reddit_data():
    """Test OpenAI with simulated Reddit data"""
    print("\nTesting OpenAI with Reddit data simulation...")
    
    # Simulate Reddit data
    fake_reddit_data = """
    Post Title: I love programming
    Post Body: Just learned Python and it's amazing!
    Comment: Thanks for the help everyone
    Comment: This community is great
    """
    
    username = "testuser"
    
    try:
        system_prompt = "You are a helpful assistant that analyzes Reddit user histories."
        user_prompt = f"""
        Please analyze the following Reddit data from user u/{username}:
        
        {fake_reddit_data}
        
        Provide a brief 2-sentence summary of their interests.
        """
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=100,
            temperature=0.5,
            api_key=OPENAI_API_KEY
        )
        
        result = response.choices[0].message.content
        print(f"SUCCESS: {result}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("OpenAI API Test Suite")
    print("=" * 40)
    
    test1 = test_openai_basic()
    test2 = test_openai_with_reddit_data()
    
    print("\n" + "=" * 40)
    print(f"Results: {sum([test1, test2])}/2 tests passed")
    
    if test1 and test2:
        print("All OpenAI tests passed!")
    else:
        print("Some tests failed. Check the errors above.")
