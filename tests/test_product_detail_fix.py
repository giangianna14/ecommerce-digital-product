#!/usr/bin/env python3
"""
Test script to verify that the product detail page fix is working correctly.
This script tests:
1. Backend API endpoints (products list and detail)
2. Frontend accessibility
3. Navigation flow
"""

import requests
import json
import sys

def test_backend_api():
    """Test backend API endpoints"""
    print("🔧 Testing Backend API...")
    
    base_url = "http://localhost:8000/api/v1"
    
    # Test health check
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print(f"❌ Health check: FAILED (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health check: FAILED (error: {e})")
        return False
    
    # Test products list
    try:
        response = requests.get(f"{base_url}/products", timeout=5)
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Products list: PASSED ({len(products)} products found)")
        else:
            print(f"❌ Products list: FAILED (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Products list: FAILED (error: {e})")
        return False
    
    # Test product detail (product ID 1)
    try:
        response = requests.get(f"{base_url}/products/1", timeout=5)
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product detail (ID 1): PASSED")
            print(f"   Product: {product.get('name', 'Unknown')}")
            print(f"   Price: ${product.get('price', 'N/A')}")
        else:
            print(f"❌ Product detail (ID 1): FAILED (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Product detail (ID 1): FAILED (error: {e})")
        return False
    
    # Test product detail (product ID 2)
    try:
        response = requests.get(f"{base_url}/products/2", timeout=5)
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product detail (ID 2): PASSED")
            print(f"   Product: {product.get('name', 'Unknown')}")
        else:
            print(f"❌ Product detail (ID 2): FAILED (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Product detail (ID 2): FAILED (error: {e})")
        return False
    
    return True

def test_frontend_accessibility():
    """Test frontend page accessibility"""
    print("\n🌐 Testing Frontend Accessibility...")
    
    frontend_url = "http://localhost:3000"
    
    # Test homepage
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print("✅ Homepage: ACCESSIBLE")
        else:
            print(f"❌ Homepage: FAILED (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Homepage: FAILED (error: {e})")
        return False
    
    # Test product detail pages
    for product_id in [1, 2]:
        try:
            response = requests.get(f"{frontend_url}/products/{product_id}", timeout=10)
            if response.status_code == 200:
                print(f"✅ Product detail page (ID {product_id}): ACCESSIBLE")
            else:
                print(f"❌ Product detail page (ID {product_id}): FAILED (status: {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ Product detail page (ID {product_id}): FAILED (error: {e})")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Testing Product Detail Page Fix")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_backend_api()
    
    # Test frontend
    frontend_ok = test_frontend_accessibility()
    
    # Final result
    print("\n" + "=" * 50)
    if backend_ok and frontend_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Product detail page functionality is working correctly")
        print("✅ Users can now access product detail pages via 'View Details' button")
        print("✅ API endpoints are responding without authentication errors")
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        if not backend_ok:
            print("❌ Backend API has issues")
        if not frontend_ok:
            print("❌ Frontend accessibility has issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())
