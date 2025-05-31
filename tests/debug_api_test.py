#!/usr/bin/env python3
"""
Debug script to test API responses and identify the issue with product detail page
"""

import requests
import json

def test_api_detailed():
    """Test API in detail to debug the frontend issue"""
    print("🔍 DEBUG: Testing API in detail")
    print("=" * 50)
    
    # Test backend health
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Backend health: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend health: {e}")
        return
    
    # Test products list
    try:
        response = requests.get("http://localhost:8000/api/v1/products", timeout=5)
        print(f"✅ Products list: {response.status_code}")
        products = response.json()
        print(f"   Found {len(products)} products")
        if products:
            first_product = products[0]
            print(f"   First product ID: {first_product.get('id')}")
            print(f"   First product name: {first_product.get('name')}")
    except Exception as e:
        print(f"❌ Products list: {e}")
        return
    
    # Test specific product detail
    for product_id in [1, 2]:
        try:
            response = requests.get(f"http://localhost:8000/api/v1/products/{product_id}", timeout=5)
            print(f"✅ Product {product_id} detail: {response.status_code}")
            
            if response.status_code == 200:
                product = response.json()
                print(f"   ID: {product.get('id')}")
                print(f"   Name: {product.get('name')}")
                print(f"   Price: ${product.get('price')}")
                print(f"   Active: {product.get('is_active')}")
                print(f"   Digital: {product.get('is_digital')}")
                
                # Check if it has all required fields
                required_fields = ['id', 'name', 'price', 'is_active', 'is_digital']
                missing_fields = [field for field in required_fields if field not in product]
                if missing_fields:
                    print(f"   ⚠️  Missing fields: {missing_fields}")
                else:
                    print(f"   ✅ All required fields present")
            else:
                print(f"   Error response: {response.text}")
                
        except Exception as e:
            print(f"❌ Product {product_id} detail: {e}")
    
    # Test frontend connectivity
    print("\n🌐 Testing Frontend...")
    try:
        response = requests.get("http://localhost:3001", timeout=5)
        print(f"✅ Frontend home: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend home: {e}")
        
    try:
        response = requests.get("http://localhost:3001/products/1", timeout=5)
        print(f"✅ Frontend product page: {response.status_code}")
        if response.status_code == 200:
            content = response.text
            if "loading" in content.lower():
                print("   ⚠️  Page shows loading state")
            if "error" in content.lower():
                print("   ⚠️  Page shows error state")
            if "product not found" in content.lower():
                print("   ⚠️  Page shows 'product not found'")
    except Exception as e:
        print(f"❌ Frontend product page: {e}")

if __name__ == "__main__":
    test_api_detailed()
