from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ProductCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    slug: str = Field(..., min_length=1, max_length=100)


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None


class ProductCategory(ProductCategoryBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=500)
    slug: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., ge=0)
    original_price: Optional[Decimal] = Field(None, ge=0)
    is_free: bool = False
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=500)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[Decimal] = Field(None, ge=0)
    original_price: Optional[Decimal] = Field(None, ge=0)
    is_free: Optional[bool] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    category_id: Optional[int] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[str] = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    is_featured: bool
    is_digital: bool
    thumbnail: Optional[str] = None
    images: Optional[str] = None  # JSON string
    preview_file: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    download_limit: int
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[str] = None
    download_count: int
    view_count: int
    purchase_count: int
    rating: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[ProductCategory] = None


class ProductList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    short_description: Optional[str] = None
    slug: str
    price: Decimal
    original_price: Optional[Decimal] = None
    is_free: bool
    is_featured: bool
    thumbnail: Optional[str] = None
    rating: Decimal
    purchase_count: int
    category: Optional[ProductCategory] = None


class ProductSearch(BaseModel):
    query: Optional[str] = None
    category_id: Optional[int] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    is_featured: Optional[bool] = None
    is_free: Optional[bool] = None
