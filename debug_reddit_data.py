"""
Debug Reddit data fetching for sproinkerino
"""

import asyncio
import asyncpraw
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

async def debug_reddit_fetch():
    """Debug the Reddit data fetching process"""
    print("🔍 Debugging Reddit Data Fetch for sproinkerino")
    print("="*60)
    
    print(f"Reddit Client ID: {REDDIT_CLIENT_ID[:10]}..." if REDDIT_CLIENT_ID else "❌ Not set")
    print(f"Reddit Client Secret: {'✅ Set' if REDDIT_CLIENT_SECRET else '❌ Not set'}")
    print(f"Reddit User Agent: {REDDIT_USER_AGENT}")
    print("="*60)
    
    try:
        # Initialize AsyncPRAW
        reddit = asyncpraw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )
        
        print("✅ Reddit client initialized")
        
        # Try to get the redditor
        username = "sproinkerino"
        print(f"🔍 Fetching data for u/{username}...")
        
        redditor = await reddit.redditor(username)
        print("✅ Redditor object created")
        
        # Check if user exists by loading the redditor
        try:
            # Load the redditor to check if it exists
            await redditor.load()
            print(f"✅ User exists: u/{redditor.name}")
        except Exception as e:
            print(f"❌ User might not exist or is private: {e}")
            await reddit.close()
            return
        
        content = []
        
        # Fetch recent submissions
        print("📝 Fetching recent submissions...")
        submission_count = 0
        async for submission in redditor.submissions.new(limit=10):
            submission_count += 1
            content.append(f"Post Title: {submission.title}")
            if submission.selftext:
                content.append(f"Post Body: {submission.selftext}")
            print(f"  Found submission {submission_count}: {submission.title[:50]}...")
        
        print(f"📝 Total submissions found: {submission_count}")
        
        # Fetch recent comments
        print("💬 Fetching recent comments...")
        comment_count = 0
        async for comment in redditor.comments.new(limit=100):
            comment_count += 1
            content.append(f"Comment: {comment.body}")
            if comment_count <= 3:  # Show first 3 comments
                print(f"  Found comment {comment_count}: {comment.body[:50]}...")
        
        print(f"💬 Total comments found: {comment_count}")
        
        if not content:
            print("❌ No content found for this user!")
            print("Possible reasons:")
            print("- User has no public posts/comments")
            print("- User account is private/suspended")
            print("- User account doesn't exist")
        else:
            print(f"✅ Total content items: {len(content)}")
            print("📄 Sample content:")
            for i, item in enumerate(content[:3]):
                print(f"  {i+1}. {item[:100]}...")
        
        await reddit.close()
        
    except Exception as e:
        print(f"❌ Error during Reddit fetch: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(debug_reddit_fetch())
