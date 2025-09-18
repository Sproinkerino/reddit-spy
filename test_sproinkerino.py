"""
Test the production API with specific inputs for sproinkerino user
"""

import requests
import json

PRODUCTION_URL = "https://reddit-spy.onrender.com"

def test_sproinkerino_analysis():
    """Test analysis with the specific inputs provided"""
    print("🔍 Testing Production API with sproinkerino")
    print(f"API URL: {PRODUCTION_URL}")
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
    
    print("📋 Request Details:")
    print(f"User ID: {payload['user_id']}")
    print(f"User to Search: u/{payload['user_to_search']}")
    print(f"Model: {payload['parameters']['model']}")
    print(f"Post Limit: {payload['parameters']['post_limit']}")
    print(f"Comment Limit: {payload['parameters']['comment_limit']}")
    print(f"Temperature: {payload['parameters']['temperature']}")
    print(f"Custom Prompt: '{payload['parameters']['custom_prompt'].strip()}'")
    print("="*80)
    
    try:
        print("🚀 Sending request to production API...")
        response = requests.post(f"{PRODUCTION_URL}/analyze", json=payload, timeout=120)
        
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
            
    except requests.exceptions.Timeout:
        print("\n⏰ REQUEST TIMEOUT!")
        print("The analysis took longer than 2 minutes. This might be due to:")
        print("- Large amount of data to process")
        print("- High server load")
        print("- Network issues")
        return False
    except Exception as e:
        print(f"\n❌ REQUEST ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_sproinkerino_analysis()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")
