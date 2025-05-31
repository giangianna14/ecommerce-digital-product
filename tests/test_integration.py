#!/usr/bin/env python3
"""
Integration test script to verify the full e-commerce platform is working
"""

import requests
import json
import time
from typing import Dict, Any

def test_backend_api():
    """Test backend API endpoints"""
    print("🧪 Testing Backend API...")
    
    base_url = "http://localhost:8000/api/v1"
    
    tests = [
        {
            "name": "Health Check",
            "url": "http://localhost:8000/health",
            "expected_status": 200
        },
        {
            "name": "Products List",
            "url": f"{base_url}/products/",
            "expected_status": 200,
            "check_data": lambda data: isinstance(data, list) and len(data) > 0
        },
        {
            "name": "Product Categories",
            "url": f"{base_url}/products/categories",
            "expected_status": 200,
            "check_data": lambda data: isinstance(data, list) and len(data) > 0
        },
        {
            "name": "Featured Products",
            "url": f"{base_url}/products/featured",
            "expected_status": 200,
            "check_data": lambda data: isinstance(data, list) and len(data) > 0
        }
    ]
    
    for test in tests:
        try:
            response = requests.get(test["url"], timeout=5)
            
            if response.status_code == test["expected_status"]:
                if "check_data" in test:
                    data = response.json()
                    if test["check_data"](data):
                        print(f"  ✅ {test['name']}: PASSED")
                    else:
                        print(f"  ❌ {test['name']}: FAILED (invalid data)")
                        print(f"     Data: {data}")
                else:
                    print(f"  ✅ {test['name']}: PASSED")
            else:
                print(f"  ❌ {test['name']}: FAILED (status {response.status_code})")
                print(f"     Response: {response.text[:200]}")
                
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {test['name']}: FAILED (connection error)")
            print(f"     Error: {e}")

def test_frontend():
    """Test frontend availability"""
    print("\n🌐 Testing Frontend...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            if "Digital Product Store" in response.text:
                print("  ✅ Frontend Loading: PASSED")
            else:
                print("  ❌ Frontend Loading: FAILED (unexpected content)")
        else:
            print(f"  ❌ Frontend Loading: FAILED (status {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Frontend Loading: FAILED (connection error)")
        print(f"     Error: {e}")

def test_cors():
    """Test CORS configuration"""
    print("\n🔗 Testing CORS...")
    
    try:
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type"
        }
        
        response = requests.options("http://localhost:8000/api/v1/products/", headers=headers, timeout=5)
        
        if response.status_code == 200:
            print("  ✅ CORS Preflight: PASSED")
            
            # Test actual request with CORS headers
            headers = {"Origin": "http://localhost:3000"}
            response = requests.get("http://localhost:8000/api/v1/products/", headers=headers, timeout=5)
            
            if response.status_code == 200:
                print("  ✅ CORS Request: PASSED")
            else:
                print(f"  ❌ CORS Request: FAILED (status {response.status_code})")
        else:
            print(f"  ❌ CORS Preflight: FAILED (status {response.status_code})")
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ CORS Test: FAILED (connection error)")
        print(f"     Error: {e}")

def test_sample_data():
    """Test that sample data was created correctly"""
    print("\n📊 Testing Sample Data...")
    
    try:
        # Test products
        response = requests.get("http://localhost:8000/api/v1/products/", timeout=5)
        products = response.json()
        
        expected_products = [
            "React Admin Dashboard Template",
            "Vue.js E-commerce Template", 
            "Flutter Mobile App UI Kit",
            "Free HTML5 Landing Page Template"
        ]
        
        found_products = [p["name"] for p in products]
        
        for expected in expected_products:
            if expected in found_products:
                print(f"  ✅ Product '{expected}': FOUND")
            else:
                print(f"  ❌ Product '{expected}': NOT FOUND")
        
        # Test categories
        response = requests.get("http://localhost:8000/api/v1/products/categories", timeout=5)
        categories = response.json()
        
        expected_categories = ["Web Development", "Mobile Apps", "Design Assets", "E-books", "Software Tools"]
        found_categories = [c["name"] for c in categories]
        
        for expected in expected_categories:
            if expected in found_categories:
                print(f"  ✅ Category '{expected}': FOUND")
            else:
                print(f"  ❌ Category '{expected}': NOT FOUND")
                
        # Test featured products
        response = requests.get("http://localhost:8000/api/v1/products/featured", timeout=5)
        featured = response.json()
        
        if len(featured) >= 3:
            print(f"  ✅ Featured Products: FOUND ({len(featured)} products)")
        else:
            print(f"  ❌ Featured Products: INSUFFICIENT ({len(featured)} products)")
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Sample Data Test: FAILED (connection error)")
        print(f"     Error: {e}")
    except json.JSONDecodeError as e:
        print(f"  ❌ Sample Data Test: FAILED (invalid JSON)")
        print(f"     Error: {e}")

def main():
    """Run all integration tests"""
    print("🚀 E-commerce Platform Integration Test")
    print("=" * 50)
    
    test_backend_api()
    test_frontend()
    test_cors()
    test_sample_data()
    
    print("\n" + "=" * 50)
    print("✨ Integration test completed!")
    print("\n📝 Quick Access URLs:")
    print("   • Frontend: http://localhost:3000")
    print("   • API Documentation: http://localhost:8000/api/v1/docs")
    print("   • Admin Login: admin@example.com / admin123")

if __name__ == "__main__":
    main()

# Kredensial admin untuk testing:
# Email: admin@example.com
# Password: admin123
