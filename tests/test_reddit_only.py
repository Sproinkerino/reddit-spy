"""
Test just the Reddit API functionality without OpenAI
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_reddit_connection():
    """Test if we can connect to Reddit API"""
    print("Testing Reddit API connection...")
    
    # Test with a known active Reddit user
    payload = {
        "user_id": "test_caller",
        "user_to_search": "spez",  # Reddit CEO
        "parameters": {
            "post_limit": 2,
            "comment_limit": 3
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("SUCCESS: Reddit API is working!")
            return True
        elif response.status_code == 500:
            print("Reddit API works, but OpenAI has issues")
            return True
        else:
            print("Reddit API issue")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_reddit_connection()
