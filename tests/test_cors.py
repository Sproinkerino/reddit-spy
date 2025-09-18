"""
Test CORS functionality for frontend communication
"""

import requests
import json

def test_cors_headers():
    """Test that CORS headers are properly set"""
    print("Testing CORS headers...")
    
    # Test OPTIONS request (preflight)
    try:
        response = requests.options(
            "https://reddit-spy.onrender.com/analyze",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        print(f"OPTIONS Status Code: {response.status_code}")
        print("CORS Headers:")
        for header, value in response.headers.items():
            if "access-control" in header.lower():
                print(f"  {header}: {value}")
        
        if "access-control-allow-origin" in response.headers:
            print("✅ CORS preflight request successful!")
            return True
        else:
            print("❌ CORS headers missing!")
            return False
            
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def test_cors_with_origin():
    """Test actual request with Origin header"""
    print("\nTesting CORS with Origin header...")
    
    payload = {
        "user_id": "cors_test_user",
        "user_to_search": "spez",
        "parameters": {
            "post_limit": 1,
            "comment_limit": 1
        }
    }
    
    try:
        response = requests.post(
            "https://reddit-spy.onrender.com/analyze",
            json=payload,
            headers={
                "Origin": "http://localhost:3000",
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        print(f"POST Status Code: {response.status_code}")
        print("Response CORS Headers:")
        for header, value in response.headers.items():
            if "access-control" in header.lower():
                print(f"  {header}: {value}")
        
        if response.status_code == 200:
            print("✅ CORS request successful!")
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CORS request failed: {e}")
        return False

def test_multiple_origins():
    """Test different frontend origins"""
    print("\nTesting multiple frontend origins...")
    
    origins = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "https://your-frontend-domain.com"
    ]
    
    success_count = 0
    
    for origin in origins:
        try:
            response = requests.options(
                "https://reddit-spy.onrender.com/analyze",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": "POST"
                }
            )
            
            if "access-control-allow-origin" in response.headers:
                print(f"✅ {origin} - CORS allowed")
                success_count += 1
            else:
                print(f"❌ {origin} - CORS not allowed")
                
        except Exception as e:
            print(f"❌ {origin} - Error: {e}")
    
    print(f"\nCORS Results: {success_count}/{len(origins)} origins allowed")
    return success_count > 0

if __name__ == "__main__":
    print("🌐 CORS Functionality Test")
    print("Testing frontend communication with Reddit Stalker API")
    print("=" * 60)
    
    test1 = test_cors_headers()
    test2 = test_cors_with_origin()
    test3 = test_multiple_origins()
    
    print("\n" + "=" * 60)
    print(f"📊 CORS Test Results: {sum([test1, test2, test3])}/3 tests passed")
    
    if all([test1, test2, test3]):
        print("🎉 All CORS tests passed! Your frontend can communicate with the API!")
    else:
        print("⚠️ Some CORS tests failed. Check the configuration.")
