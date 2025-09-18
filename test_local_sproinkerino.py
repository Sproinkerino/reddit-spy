"""
Test the local API with sproinkerino data
"""

import requests
import json

LOCAL_URL = "http://localhost:8000"

def test_local_sproinkerino():
    """Test local API with sproinkerino data"""
    print("🔍 Testing Local API with sproinkerino")
    print(f"API URL: {LOCAL_URL}")
    print("="*80)
    
    # Exact payload from user
    payload = {
        "user_id": "fcc22fea-fa5d-437c-a6dd-efc591575a73",
        "user_to_search": "sproinkerino",
        "parameters": {
            "comment_limit": 100,
            "custom_prompt": "tell me about the user\n",
            "model": "gpt-4o",
            "post_limit": 10,
            "temperature": 0.5
        }
    }
    
    try:
        print("🚀 Sending request to local API...")
        response = requests.post(f"{LOCAL_URL}/analyze", json=payload, timeout=120)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ ANALYSIS SUCCESSFUL!")
            print("="*80)
            print(f"User: u/{result['analyzed_user']}")
            print(f"Analysis ID: {result['user_id']}")
            print(f"Success: {result['success']}")
            print("\n🤖 AI Analysis Results:")
            print("-"*50)
            print(result['summary'])
            print("="*80)
            return True
        else:
            print(f"\n❌ ANALYSIS FAILED!")
            print(f"Status Code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error Details: {error_data}")
            except:
                print(f"Raw Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ REQUEST ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_local_sproinkerino()
    if success:
        print("\n🎉 Local test completed successfully!")
    else:
        print("\n💥 Local test failed!")
