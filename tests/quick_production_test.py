"""
Quick production API test - Simple health check and basic functionality test
"""

import requests
import json

PRODUCTION_URL = "https://reddit-spy.onrender.com"

def quick_test():
    """Quick test of the production API"""
    print("🔍 Quick Production API Test")
    print(f"Testing: {PRODUCTION_URL}")
    print("-" * 40)
    
    # Test 1: Health Check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{PRODUCTION_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed: {data['message']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: Basic Analysis
    print("2. Testing basic analysis...")
    try:
        payload = {
            "user_id": "quick_test_user",
            "user_to_search": "spez",
            "parameters": {
                "post_limit": 1,
                "comment_limit": 2
            }
        }
        
        response = requests.post(f"{PRODUCTION_URL}/analyze", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Analysis successful for u/{data['analyzed_user']}")
            print(f"   📝 Summary preview: {data['summary'][:100]}...")
        else:
            print(f"   ❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Analysis error: {e}")
        return False
    
    print("-" * 40)
    print("🎉 Quick test completed successfully!")
    print("Your production API is working correctly!")
    return True

if __name__ == "__main__":
    quick_test()
