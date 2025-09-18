"""
Test cases for Reddit Stalker API
Run with: python test_api.py
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        print("Health check passed!\n")
        return True
    except Exception as e:
        print(f"Health check failed: {e}\n")
        return False

def test_analyze_basic():
    """Test basic user analysis"""
    print("Testing basic user analysis...")
    
    payload = {
        "user_id": "test_caller_123",
        "user_to_search": "spez",  # Reddit CEO, should have public activity
        "parameters": {
            "post_limit": 5,
            "comment_limit": 10
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"User ID: {result['user_id']}")
            print(f"Analyzed User: {result['analyzed_user']}")
            print(f"Summary Preview: {result['summary'][:200]}...")
            print("Basic analysis test passed!\n")
            return True
        else:
            print(f"Response: {response.json()}")
            print("Basic analysis test failed!\n")
            return False
            
    except Exception as e:
        print(f"Basic analysis test failed: {e}\n")
        return False

def test_analyze_with_custom_parameters():
    """Test analysis with custom parameters"""
    print("🔍 Testing analysis with custom parameters...")
    
    payload = {
        "user_id": "test_caller_456",
        "user_to_search": "spez",
        "parameters": {
            "post_limit": 3,
            "comment_limit": 5,
            "model": "gpt-4o",
            "temperature": 0.7,
            "custom_prompt": "Analyze user u/{username} and focus only on their technical interests. Data: {user_data}"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Custom Analysis Preview: {result['summary'][:200]}...")
            print("✅ Custom parameters test passed!\n")
            return True
        else:
            print(f"Response: {response.json()}")
            print("❌ Custom parameters test failed!\n")
            return False
            
    except Exception as e:
        print(f"❌ Custom parameters test failed: {e}\n")
        return False

def test_analyze_invalid_user():
    """Test analysis with invalid/non-existent user"""
    print("🔍 Testing analysis with invalid user...")
    
    payload = {
        "user_id": "test_caller_789",
        "user_to_search": "this_user_definitely_does_not_exist_12345",
        "parameters": {
            "post_limit": 5,
            "comment_limit": 10
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Should return 400 error for invalid user
        if response.status_code == 400:
            print("✅ Invalid user test passed (correctly returned error)!\n")
            return True
        else:
            print("❌ Invalid user test failed (should have returned 400)!\n")
            return False
            
    except Exception as e:
        print(f"❌ Invalid user test failed: {e}\n")
        return False

def test_analyze_missing_fields():
    """Test analysis with missing required fields"""
    print("🔍 Testing analysis with missing fields...")
    
    # Missing user_to_search field
    payload = {
        "user_id": "test_caller_999",
        "parameters": {
            "post_limit": 5
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Should return 422 validation error
        if response.status_code == 422:
            print("✅ Missing fields test passed (correctly returned validation error)!\n")
            return True
        else:
            print("❌ Missing fields test failed (should have returned 422)!\n")
            return False
            
    except Exception as e:
        print(f"❌ Missing fields test failed: {e}\n")
        return False

def run_all_tests():
    """Run all test cases"""
    print("🚀 Starting Reddit Stalker API Tests\n")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_analyze_basic,
        test_analyze_with_custom_parameters,
        test_analyze_invalid_user,
        test_analyze_missing_fields
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    print("Reddit Stalker API Test Suite")
    print("Make sure the API server is running on http://localhost:8000")
    print("Start server with: python main.py")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print("✅ Server is running, starting tests...\n")
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start it with: python main.py")
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
