#!/usr/bin/env python3
"""
Final Platform Verification Script
Memverifikasi bahwa semua komponen platform berfungsi dengan benar
"""

import requests
import json
from datetime import datetime

def verify_platform():
    """Verify all platform components are working correctly"""
    
    print("🔍 E-commerce Platform Final Verification")
    print("=" * 50)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        "backend_health": False,
        "frontend_accessible": False,
        "api_products": False,
        "api_categories": False,
        "product_detail": False,
        "price_formatting": False
    }
    
    # 1. Backend Health Check
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "healthy":
            results["backend_health"] = True
            print("✅ Backend API: Healthy (Port 8000)")
        else:
            print("❌ Backend API: Unhealthy")
    except:
        print("❌ Backend API: Not accessible")
    
    # 2. Frontend Accessibility
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            results["frontend_accessible"] = True
            print("✅ Frontend: Accessible (Port 3000)")
        else:
            print("❌ Frontend: Not accessible")
    except:
        print("❌ Frontend: Not accessible")
    
    # 3. API Products Endpoint
    try:
        response = requests.get("http://localhost:8000/api/v1/products/", timeout=5)
        if response.status_code == 200:
            products = response.json()
            if len(products) > 0:
                results["api_products"] = True
                print(f"✅ Products API: Working ({len(products)} products)")
            else:
                print("⚠️ Products API: Working but no products found")
        else:
            print("❌ Products API: Error")
    except:
        print("❌ Products API: Not accessible")
    
    # 4. API Categories Endpoint
    try:
        response = requests.get("http://localhost:8000/api/v1/products/categories", timeout=5)
        if response.status_code == 200:
            categories = response.json()
            if len(categories) > 0:
                results["api_categories"] = True
                print(f"✅ Categories API: Working ({len(categories)} categories)")
            else:
                print("⚠️ Categories API: Working but no categories found")
        else:
            print("❌ Categories API: Error")
    except:
        print("❌ Categories API: Not accessible")
    
    # 5. Product Detail Endpoint (Test with product ID 1)
    try:
        response = requests.get("http://localhost:8000/api/v1/products/1", timeout=5)
        if response.status_code == 200:
            product = response.json()
            if "name" in product and "price" in product:
                results["product_detail"] = True
                print(f"✅ Product Detail API: Working (Product: {product['name']})")
                
                # 6. Price Formatting Check
                price = product.get("price")
                if isinstance(price, str) and price.replace(".", "").replace(",", "").isdigit():
                    results["price_formatting"] = True
                    print(f"✅ Price Format: Correct (Price: ${price})")
                else:
                    print(f"⚠️ Price Format: Unexpected format (Price: {price})")
            else:
                print("❌ Product Detail API: Invalid response format")
        else:
            print("❌ Product Detail API: Error")
    except:
        print("❌ Product Detail API: Not accessible")
    
    # Summary
    print()
    print("📊 VERIFICATION SUMMARY")
    print("=" * 30)
    
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    for check, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check.replace('_', ' ').title()}")
    
    print()
    print(f"📈 Overall Status: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 STATUS: ALL SYSTEMS OPERATIONAL - PRODUCTION READY!")
    elif passed_checks >= total_checks * 0.8:
        print("⚠️ STATUS: MOSTLY OPERATIONAL - Minor issues detected")
    else:
        print("❌ STATUS: CRITICAL ISSUES - Platform needs attention")
    
    # Platform URLs
    print()
    print("🌐 PLATFORM ACCESS URLS")
    print("=" * 25)
    print("🏠 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🛍️ Product Example: http://localhost:3000/products/1")
    
    # Quick Start Commands
    print()
    print("🚀 QUICK START COMMANDS")
    print("=" * 23)
    print("# Start both servers:")
    print("npm run dev")
    print()
    print("# Or start separately:")
    print("# Backend: cd backend && uvicorn app.main:app --reload")
    print("# Frontend: cd frontend && npm start")
    
    return passed_checks == total_checks

if __name__ == "__main__":
    verify_platform()
