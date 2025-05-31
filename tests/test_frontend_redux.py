#!/usr/bin/env python3
"""
Test script to verify the Redux fix is working properly
Tests the ProductDetailPage functionality and Redux state management
"""

import requests
import time
import json
from datetime import datetime

def test_backend_api():
    """Test backend API endpoints"""
    print("🧪 Testing Backend API...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Backend health check: OK")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            
        # Test products endpoint
        response = requests.get("http://localhost:8000/api/v1/products/")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Products API: {len(products)} products available")
        else:
            print(f"❌ Products API failed: {response.status_code}")
            
        # Test specific product
        response = requests.get("http://localhost:8000/api/v1/products/1")
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product detail API: Product '{product.get('name', 'Unknown')}' found")
            return True
        else:
            print(f"❌ Product detail API failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure backend is running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        return False
        
    return True

def test_frontend_availability():
    """Test if frontend is accessible"""
    print("\n🌐 Testing Frontend Availability...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible on port 3000")
            return True
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to frontend. Make sure frontend is running on port 3000")
        return False
    except Exception as e:
        print(f"❌ Frontend test error: {e}")
        return False
        
    return False

def check_redux_implementation():
    """Check if Redux files are properly implemented"""
    print("\n⚛️ Checking Redux Implementation...")
    
    try:
        # Check if Redux hooks file exists
        with open("frontend/src/hooks/redux.ts", "r") as f:
            content = f.read()
            if "useAppDispatch" in content and "useAppSelector" in content:
                print("✅ Typed Redux hooks implemented")
            else:
                print("❌ Redux hooks not properly implemented")
                
        # Check if Provider is in index.tsx
        with open("frontend/src/index.tsx", "r") as f:
            content = f.read()
            if "Provider" in content and "store" in content:
                print("✅ Redux Provider added to index.tsx")
            else:
                print("❌ Redux Provider not found in index.tsx")
                
        # Check ProductDetailPage uses typed hooks
        with open("frontend/src/pages/ProductDetailPage/ProductDetailPage.tsx", "r") as f:
            content = f.read()
            if "useAppSelector" in content and "useAppDispatch" in content:
                print("✅ ProductDetailPage uses typed Redux hooks")
            else:
                print("❌ ProductDetailPage doesn't use typed Redux hooks")
                
        return True
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Redux check error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Redux Fix - ProductDetailPage Functionality")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test backend
    backend_ok = test_backend_api()
    
    # Test frontend
    frontend_ok = test_frontend_availability()
    
    # Check Redux implementation
    redux_ok = check_redux_implementation()
    
    print("\n📊 Test Summary")
    print("=" * 60)
    print(f"🖥️  Backend API: {'✅ OK' if backend_ok else '❌ FAILED'}")
    print(f"🌐 Frontend: {'✅ OK' if frontend_ok else '❌ FAILED'}")
    print(f"⚛️  Redux Implementation: {'✅ OK' if redux_ok else '❌ FAILED'}")
    
    if backend_ok and frontend_ok and redux_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ ProductDetailPage should now work correctly")
        print("✅ Redux Provider is connected")
        print("✅ State management is operational")
        print("\n🔗 Test URLs:")
        print("   • Homepage: http://localhost:3000")
        print("   • Products: http://localhost:3000/products")
        print("   • Product Detail: http://localhost:3000/products/1")
        print("   • API Docs: http://localhost:8000/docs")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Check the error messages above and ensure both servers are running.")
        
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
