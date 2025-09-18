"""
Test OpenAI API using direct HTTP requests to bypass package conflicts
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def test_openai_direct():
    """Test OpenAI API using direct HTTP requests"""
    print("Testing OpenAI API with direct HTTP requests...")
    
    if not OPENAI_API_KEY:
        print("ERROR: No OpenAI API key found")
        return False
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say 'Direct HTTP request works!'"}
        ],
        "max_tokens": 50,
        "temperature": 0.5
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"SUCCESS: {message}")
            return True
        else:
            print(f"ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_openai_with_reddit_simulation():
    """Test OpenAI with simulated Reddit data using direct requests"""
    print("\nTesting OpenAI with Reddit data simulation...")
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Simulate Reddit data
    fake_reddit_data = """
    Post Title: I love programming
    Post Body: Just learned Python and it's amazing!
    Comment: Thanks for the help everyone
    Comment: This community is great
    """
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system", 
                "content": "You are a helpful assistant that analyzes Reddit user histories."
            },
            {
                "role": "user", 
                "content": f"Please analyze this Reddit data from user u/testuser and provide a brief 2-sentence summary of their interests:\n\n{fake_reddit_data}"
            }
        ],
        "max_tokens": 100,
        "temperature": 0.5
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"SUCCESS: {message}")
            return True
        else:
            print(f"ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("OpenAI Direct HTTP Test")
    print("=" * 40)
    
    test1 = test_openai_direct()
    test2 = test_openai_with_reddit_simulation()
    
    print("\n" + "=" * 40)
    print(f"Results: {sum([test1, test2])}/2 tests passed")
    
    if test1 and test2:
        print("All tests passed! OpenAI API is working via direct HTTP requests.")
    else:
        print("Some tests failed.")
