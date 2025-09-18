"""
Debug OpenAI API issues
"""

import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def debug_openai():
    """Debug OpenAI configuration"""
    print("=== OpenAI Debug Information ===")
    print(f"OpenAI version: {openai.__version__}")
    print(f"API Key present: {'Yes' if OPENAI_API_KEY else 'No'}")
    print(f"API Key length: {len(OPENAI_API_KEY) if OPENAI_API_KEY else 0}")
    
    # Check for proxy-related environment variables
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']
    print("\nProxy environment variables:")
    for var in proxy_vars:
        value = os.getenv(var)
        if value:
            print(f"  {var}: {value}")
        else:
            print(f"  {var}: Not set")
    
    # Try to create a client manually
    print("\n=== Testing Client Creation ===")
    try:
        # Try without any extra arguments
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        print("SUCCESS: Client created without extra arguments")
        
        # Test a simple call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print(f"SUCCESS: API call worked - {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        print(f"Error type: {type(e)}")
        
        # Try with explicit parameters
        try:
            print("\nTrying with explicit parameters...")
            client = openai.OpenAI(
                api_key=OPENAI_API_KEY,
                timeout=30.0
            )
            print("SUCCESS: Client created with explicit timeout")
            return True
        except Exception as e2:
            print(f"ERROR with explicit params: {e2}")
            return False

if __name__ == "__main__":
    debug_openai()
