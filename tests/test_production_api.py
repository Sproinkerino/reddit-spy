"""
Test file for the production Reddit Stalker API deployed on Render
Tests the live API at https://reddit-spy.onrender.com
"""

import requests
import json
import time

# Production API base URL
PRODUCTION_URL = "https://reddit-spy.onrender.com"

def test_production_health():
    """Test the production health check endpoint"""
    print("Testing production health check...")
    try:
        response = requests.get(f"{PRODUCTION_URL}/", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "healthy"
            print("✅ Production health check passed!")
            return True
        else:
            print("❌ Production health check failed!")
            return False
            
    except Exception as e:
        print(f"❌ Production health check failed: {e}")
        return False

def test_production_analyze_basic():
    """Test basic user analysis on production"""
    print("\nTesting production basic user analysis...")
    
    payload = {
        "user_id": "production_test_user",
        "user_to_search": "spez",  # Reddit CEO, should have public activity
        "parameters": {
            "post_limit": 3,
            "comment_limit": 5
        }
    }
    
    try:
        print("Sending request to production API...")
        response = requests.post(f"{PRODUCTION_URL}/analyze", json=payload, timeout=60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"User ID: {result['user_id']}")
            print(f"Analyzed User: {result['analyzed_user']}")
            print("\n📊 FULL ANALYSIS RESULTS:")
            print("="*80)
            print(f"User: u/{result['analyzed_user']}")
            print(f"Analysis ID: {result['user_id']}")
            print(f"Success: {result['success']}")
            print("\n🤖 AI Analysis Summary:")
            print("-"*50)
            print(result['summary'])
            print("="*80)
            print("✅ Production basic analysis test passed!")
            return True
        else:
            print(f"Response: {response.json()}")
            print("❌ Production basic analysis test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Production basic analysis test failed: {e}")
        return False

def test_production_analyze_invalid_user():
    """Test analysis with invalid user on production"""
    print("\nTesting production invalid user handling...")
    
    payload = {
        "user_id": "production_test_user",
        "user_to_search": "this_user_definitely_does_not_exist_12345",
        "parameters": {
            "post_limit": 5,
            "comment_limit": 10
        }
    }
    
    try:
        response = requests.post(f"{PRODUCTION_URL}/analyze", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Should return 400 error for invalid user
        if response.status_code == 400:
            print("✅ Production invalid user test passed (correctly returned error)!")
            return True
        else:
            print("❌ Production invalid user test failed (should have returned 400)!")
            return False
            
    except Exception as e:
        print(f"❌ Production invalid user test failed: {e}")
        return False

def test_production_analyze_missing_fields():
    """Test analysis with missing required fields on production"""
    print("\nTesting production missing fields validation...")
    
    # Missing user_to_search field
    payload = {
        "user_id": "production_test_user",
        "parameters": {
            "post_limit": 5
        }
    }
    
    try:
        response = requests.post(f"{PRODUCTION_URL}/analyze", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Should return 422 validation error
        if response.status_code == 422:
            print("✅ Production missing fields test passed (correctly returned validation error)!")
            return True
        else:
            print("❌ Production missing fields test failed (should have returned 422)!")
            return False
            
    except Exception as e:
        print(f"❌ Production missing fields test failed: {e}")
        return False

def test_production_custom_parameters():
    """Test analysis with custom parameters on production"""
    print("\nTesting production custom parameters...")
    
    payload = {
        "user_id": "production_test_user",
        "user_to_search": "spez",
        "parameters": {
            "post_limit": 2,
            "comment_limit": 3,
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "custom_prompt": "Analyze user u/{username} and focus only on their technical interests. Data: {user_data}"
        }
    }
    
    try:
        response = requests.post(f"{PRODUCTION_URL}/analyze", json=payload, timeout=60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Custom Analysis Preview: {result['summary'][:200]}...")
            print("✅ Production custom parameters test passed!")
            return True
        else:
            print(f"Response: {response.json()}")
            print("❌ Production custom parameters test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Production custom parameters test failed: {e}")
        return False

def test_production_performance():
    """Test production API performance"""
    print("\nTesting production API performance...")
    
    payload = {
        "user_id": "performance_test_user",
        "user_to_search": "spez",
        "parameters": {
            "post_limit": 1,
            "comment_limit": 2
        }
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{PRODUCTION_URL}/analyze", json=payload, timeout=60)
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"Response Time: {response_time:.2f} seconds")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200 and response_time < 30:
            print("✅ Production performance test passed!")
            return True
        else:
            print("❌ Production performance test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Production performance test failed: {e}")
        return False

def run_all_production_tests():
    """Run all production tests"""
    print("🚀 Starting Production API Tests")
    print(f"Testing API at: {PRODUCTION_URL}")
    print("=" * 60)
    
    tests = [
        test_production_health,
        test_production_analyze_basic,
        test_production_analyze_invalid_user,
        test_production_analyze_missing_fields,
        test_production_custom_parameters,
        test_production_performance
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(2)  # Small delay between tests to be nice to the server
    
    print("\n" + "=" * 60)
    print(f"📊 Production Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All production tests passed! Your API is working perfectly!")
    else:
        print("⚠️ Some production tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    print("Reddit Stalker API - Production Test Suite")
    print("Testing live API at https://reddit-spy.onrender.com")
    print()
    
    try:
        # Test if the production URL is reachable
        response = requests.get(PRODUCTION_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Production API is reachable, starting tests...\n")
            run_all_production_tests()
        else:
            print(f"❌ Production API returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to production API. Please check if it's deployed and running.")
    except requests.exceptions.Timeout:
        print("❌ Production API request timed out. The server might be slow or down.")
    except Exception as e:
        print(f"❌ Error connecting to production API: {e}")
