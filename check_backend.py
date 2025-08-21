#!/usr/bin/env python3
"""
Quick script to check which backend version is running.
"""

import requests

def check_backend():
    try:
        # Check the root endpoint
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            data = response.json()
            message = data.get("message", "")
            print(f"Backend Response: {message}")
            
            if "Simple Mode" in message:
                print("✅ CORRECT: Simple backend is running (no authentication)")
                return True
            else:
                print("❌ WRONG: Old backend is running (has authentication)")
                print("   Stop the backend and run: start_backend_simple.bat")
                return False
        else:
            print(f"❌ Backend not responding: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure backend is running on http://localhost:8000")
        return False

if __name__ == "__main__":
    print("Checking which backend version is running...")
    print("=" * 50)
    check_backend()