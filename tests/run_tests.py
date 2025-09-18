"""
Simple test runner script
Run with: python run_tests.py
"""

import subprocess
import sys
import time

def check_server():
    """Check if the API server is running"""
    import requests
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Start the API server in background"""
    print("🚀 Starting API server...")
    process = subprocess.Popen([sys.executable, "main.py"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    time.sleep(3)  # Give server time to start
    return process

def run_tests():
    """Run the test suite"""
    print("🧪 Running test suite...")
    result = subprocess.run([sys.executable, "test_api.py"], 
                           capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    return result.returncode == 0

if __name__ == "__main__":
    print("🎯 Reddit Stalker API Test Runner")
    print("=" * 40)
    
    # Check if server is already running
    if check_server():
        print("✅ Server is already running")
        run_tests()
    else:
        print("🔄 Server not detected, starting it...")
        server_process = start_server()
        
        try:
            # Wait for server to be ready
            for i in range(10):
                if check_server():
                    print("✅ Server is ready")
                    break
                time.sleep(1)
                print(f"⏳ Waiting for server... ({i+1}/10)")
            else:
                print("❌ Server failed to start")
                sys.exit(1)
            
            # Run tests
            run_tests()
            
        finally:
            # Clean up server process
            print("🛑 Stopping server...")
            server_process.terminate()
            server_process.wait()
            print("✅ Done!")
