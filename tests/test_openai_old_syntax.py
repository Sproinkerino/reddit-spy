"""
Test OpenAI with older API syntax
"""

import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def test_old_syntax():
    """Test using the older openai API syntax"""
    print("Testing OpenAI with older API syntax...")
    
    # Set the API key globally (older method)
    openai.api_key = OPENAI_API_KEY
    
    try:
        # Use the older completion API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello from OpenAI!'"}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"SUCCESS: {result}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_direct_import():
    """Test with direct import to avoid conflicts"""
    print("\nTesting with direct import...")
    
    try:
        # Import only what we need
        from openai import OpenAI
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Direct import works!'"}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"SUCCESS: {result}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("OpenAI Old Syntax Test")
    print("=" * 40)
    
    test1 = test_old_syntax()
    test2 = test_direct_import()
    
    print("\n" + "=" * 40)
    print(f"Results: {sum([test1, test2])}/2 tests passed")
