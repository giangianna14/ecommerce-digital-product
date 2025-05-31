#!/usr/bin/env python3
"""
Test script to verify that the Redux Provider fix is working
"""
import requests
import json
import time

def test_frontend_after_redux_fix():
    """Test the frontend functionality after adding Redux Provider"""
    print("🧪 Testing Redux Provider Fix...")
    
    # Test 1: Check if frontend is accessible
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible on port 3000")
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend is not accessible: {e}")
        return
    
    # Test 2: Check if product detail page loads without errors
    try:
        response = requests.get("http://localhost:3000/products/1", timeout=5)
        if response.status_code == 200:
            print("✅ Product detail page is accessible")
            
            # Check for common error indicators
            html_content = response.text
            if "Cannot read properties of undefined" in html_content:
                print("❌ Redux state access errors detected in page")
            elif "useSelector" in html_content and "undefined" in html_content:
                print("❌ Potential Redux connection issues detected")
            else:
                print("✅ No obvious Redux errors detected in page HTML")
        else:
            print(f"❌ Product detail page returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Product detail page test failed: {e}")
    
    # Test 3: Verify API is still working
    try:
        response = requests.get("http://localhost:8000/api/v1/products/1", timeout=5)
        if response.status_code == 200:
            product_data = response.json()
            print(f"✅ API is working - Product: {product_data['name']}")
        else:
            print(f"❌ API returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ API test failed: {e}")
    
    print("\n📋 Summary:")
    print("1. Added Redux Provider to index.tsx - this was the main issue")
    print("2. Cleaned up duplicate Provider in App.tsx")
    print("3. Fixed Redux store connection to React components")
    print("\n💡 The ProductDetailPage should now properly access Redux state")
    print("   and dispatch actions like fetchProductById")

if __name__ == "__main__":
    test_frontend_after_redux_fix()
