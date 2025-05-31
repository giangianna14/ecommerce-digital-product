from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_active_user, get_current_user, get_current_user_optional
from app.models.user import User
from app.schemas.product import (
    Product, ProductCreate, ProductUpdate, ProductList,
    ProductCategory, ProductCategoryCreate, ProductCategoryUpdate
)
from app.services.product_service import ProductService

router = APIRouter()


# Product Categories
@router.get("/categories", response_model=List[ProductCategory])
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all product categories"""
    product_service = ProductService(db)
    return product_service.get_categories(skip=skip, limit=limit)


@router.post("/categories", response_model=ProductCategory)
async def create_category(
    category_data: ProductCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new product category (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    product_service = ProductService(db)
    return product_service.create_category(category_data)


# Products
@router.get("/", response_model=List[ProductList])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    is_featured: Optional[bool] = Query(None),
    is_free: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get products with optional filtering"""
    product_service = ProductService(db)
    return product_service.get_products(
        skip=skip,
        limit=limit,
        category_id=category_id,
        is_featured=is_featured,
        is_free=is_free,
        search=search
    )


@router.get("/featured", response_model=List[ProductList])
async def get_featured_products(
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get featured products"""
    product_service = ProductService(db)
    return product_service.get_featured_products(limit=limit)


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get product by ID"""
    product_service = ProductService(db)
    product = product_service.get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Increment view count
    product_service.increment_view_count(product_id)
    
    return product


@router.get("/slug/{slug}", response_model=Product)
async def get_product_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get product by slug"""
    product_service = ProductService(db)
    product = product_service.get_product_by_slug(slug)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Increment view count
    product_service.increment_view_count(product.id)
    
    return product


@router.post("/", response_model=Product)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new product (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    product_service = ProductService(db)
    return product_service.create_product(product_data)


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a product (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    product_service = ProductService(db)
    product = product_service.update_product(product_id, product_data)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a product (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    product_service = ProductService(db)
    success = product_service.delete_product(product_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return {"message": "Product deleted successfully"}
