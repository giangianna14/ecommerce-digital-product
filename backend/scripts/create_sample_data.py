#!/usr/bin/env python3
"""
Create sample data for the e-commerce platform
"""

import sys
import os
from decimal import Decimal
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import base first to ensure all models are loaded
from app.db.base import Base
from app.core.database import SessionLocal, engine
from app.models.product import Product, ProductCategory
from app.models.user import User
from app.core.security import get_password_hash
from slugify import slugify


def create_sample_categories(db):
    """Create sample product categories"""
    categories_data = [
        {
            "name": "Web Development",
            "description": "Templates, themes, and resources for web development",
            "slug": "web-development"
        },
        {
            "name": "Mobile Apps",
            "description": "Mobile app templates and UI kits",
            "slug": "mobile-apps"
        },
        {
            "name": "Design Assets",
            "description": "Graphics, icons, and design resources",
            "slug": "design-assets"
        },
        {
            "name": "E-books",
            "description": "Digital books and educational content",
            "slug": "e-books"
        },
        {
            "name": "Software Tools",
            "description": "Utilities and productivity software",
            "slug": "software-tools"
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        # Check if category already exists
        existing = db.query(ProductCategory).filter(
            ProductCategory.slug == cat_data["slug"]
        ).first()
        
        if not existing:
            category = ProductCategory(**cat_data)
            db.add(category)
            categories.append(category)
            print(f"Created category: {cat_data['name']}")
        else:
            categories.append(existing)
            print(f"Category already exists: {cat_data['name']}")
    
    db.commit()
    return categories


def create_sample_products(db, categories):
    """Create sample products"""
    products_data = [
        {
            "name": "React Admin Dashboard Template",
            "description": "A comprehensive admin dashboard template built with React, TypeScript, and Tailwind CSS. Features include user management, analytics charts, dark mode, and responsive design. Perfect for SaaS applications and business dashboards.",
            "short_description": "Modern React admin dashboard with TypeScript and Tailwind CSS",
            "price": Decimal("49.99"),
            "original_price": Decimal("79.99"),
            "is_featured": True,
            "category": "Web Development",
            "file_type": "zip",
            "file_size": 15728640,  # ~15MB
            "keywords": "react, admin, dashboard, typescript, tailwind"
        },
        {
            "name": "Vue.js E-commerce Template",
            "description": "Complete e-commerce solution built with Vue.js 3, featuring shopping cart, checkout process, product catalog, user authentication, and payment integration. Includes both customer and admin interfaces.",
            "short_description": "Full-featured Vue.js e-commerce template with admin panel",
            "price": Decimal("69.99"),
            "original_price": Decimal("99.99"),
            "is_featured": True,
            "category": "Web Development",
            "file_type": "zip",
            "file_size": 25165824,  # ~24MB
            "keywords": "vue, ecommerce, shopping, cart, payment"
        },
        {
            "name": "Flutter Mobile App UI Kit",
            "description": "Beautiful mobile app UI kit for Flutter with 50+ screens including onboarding, authentication, profile, shopping, and more. Supports both iOS and Android with customizable themes.",
            "short_description": "50+ mobile app screens for Flutter development",
            "price": Decimal("39.99"),
            "category": "Mobile Apps",
            "file_type": "zip",
            "file_size": 8388608,  # ~8MB
            "keywords": "flutter, mobile, ui kit, ios, android"
        },
        {
            "name": "React Native Food Delivery App",
            "description": "Complete food delivery app template built with React Native. Includes customer app, restaurant management, and delivery tracking. Features real-time updates, payment integration, and Google Maps.",
            "short_description": "Full food delivery app solution with React Native",
            "price": Decimal("89.99"),
            "is_featured": True,
            "category": "Mobile Apps",
            "file_type": "zip",
            "file_size": 41943040,  # ~40MB
            "keywords": "react native, food delivery, maps, real-time"
        },
        {
            "name": "Premium Icon Pack - 500 Icons",
            "description": "Professional icon pack with 500 high-quality icons in multiple formats (SVG, PNG, ICO). Perfect for web and mobile applications. Includes business, technology, and general purpose icons.",
            "short_description": "500 premium icons in multiple formats",
            "price": Decimal("19.99"),
            "category": "Design Assets",
            "file_type": "zip",
            "file_size": 5242880,  # ~5MB
            "keywords": "icons, svg, png, design, graphics"
        },
        {
            "name": "Web Design Illustration Pack",
            "description": "Modern illustration pack with 30 high-quality illustrations perfect for websites, presentations, and marketing materials. Available in SVG and PNG formats with customizable colors.",
            "short_description": "30 modern web illustrations in SVG and PNG",
            "price": Decimal("29.99"),
            "category": "Design Assets",
            "file_type": "zip",
            "file_size": 12582912,  # ~12MB
            "keywords": "illustrations, web design, svg, marketing"
        },
        {
            "name": "JavaScript Mastery E-book",
            "description": "Comprehensive guide to modern JavaScript development covering ES6+, async programming, DOM manipulation, and best practices. Includes practical examples and exercises.",
            "short_description": "Complete guide to modern JavaScript development",
            "price": Decimal("24.99"),
            "category": "E-books",
            "file_type": "pdf",
            "file_size": 3145728,  # ~3MB
            "keywords": "javascript, programming, ebook, development"
        },
        {
            "name": "Free HTML5 Landing Page Template",
            "description": "Professional HTML5 landing page template perfect for startups and businesses. Fully responsive, SEO optimized, and easy to customize. Includes contact forms and smooth animations.",
            "short_description": "Professional HTML5 landing page template",
            "price": Decimal("0.00"),
            "is_free": True,
            "is_featured": True,
            "category": "Web Development",
            "file_type": "zip",
            "file_size": 2097152,  # ~2MB
            "keywords": "html5, landing page, free, responsive"
        },
        {
            "name": "Python Web Scraping Guide",
            "description": "Learn web scraping with Python using BeautifulSoup, Scrapy, and Selenium. Includes practical projects and best practices for ethical scraping.",
            "short_description": "Complete Python web scraping tutorial with projects",
            "price": Decimal("34.99"),
            "category": "E-books",
            "file_type": "pdf",
            "file_size": 4194304,  # ~4MB
            "keywords": "python, web scraping, selenium, scrapy"
        },
        {
            "name": "Code Formatter & Beautifier Tool",
            "description": "Desktop application for formatting and beautifying code in multiple languages. Supports JavaScript, Python, HTML, CSS, and more. Includes batch processing and custom formatting rules.",
            "short_description": "Multi-language code formatter desktop application",
            "price": Decimal("15.99"),
            "category": "Software Tools",
            "file_type": "exe",
            "file_size": 20971520,  # ~20MB
            "keywords": "code formatter, beautifier, desktop app, programming"
        }
    ]
    
    # Create a mapping of category names to category objects
    category_map = {cat.name: cat for cat in categories}
    
    for prod_data in products_data:
        # Check if product already exists
        slug = slugify(prod_data["name"])
        existing = db.query(Product).filter(Product.slug == slug).first()
        
        if not existing:
            # Get the category
            category_name = prod_data.pop("category")
            category = category_map.get(category_name)
            
            # Create product
            product = Product(
                name=prod_data["name"],
                description=prod_data["description"],
                short_description=prod_data["short_description"],
                slug=slug,
                price=prod_data["price"],
                original_price=prod_data.get("original_price"),
                is_free=prod_data.get("is_free", False),
                is_featured=prod_data.get("is_featured", False),
                file_type=prod_data["file_type"],
                file_size=prod_data["file_size"],
                keywords=prod_data["keywords"],
                category_id=category.id if category else None,
                meta_title=f"{prod_data['name']} - Download Now",
                meta_description=prod_data["short_description"]
            )
            
            db.add(product)
            print(f"Created product: {prod_data['name']}")
        else:
            print(f"Product already exists: {prod_data['name']}")
    
    db.commit()


def create_sample_user(db):
    """Create a sample admin user"""
    # Check if admin user already exists
    existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
    
    if not existing_admin:
        admin_user = User(
            email="admin@example.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True,
            is_verified=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Created admin user: admin@example.com (password: admin123)")
    else:
        print("Admin user already exists")


def main():
    """Main function to create all sample data"""
    print("Creating sample data for e-commerce platform...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create sample data
        print("\n1. Creating sample categories...")
        categories = create_sample_categories(db)
        
        print("\n2. Creating sample products...")
        create_sample_products(db, categories)
        
        print("\n3. Creating sample admin user...")
        create_sample_user(db)
        
        print("\n✅ Sample data created successfully!")
        print("\nYou can now:")
        print("- Browse products at: http://localhost:3000")
        print("- Access API docs at: http://localhost:8000/api/v1/docs")
        print("- Login as admin with: admin@example.com / admin123")
        
    except Exception as e:
        print(f"\n❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
