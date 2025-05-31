from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from slugify import slugify

# Import base to ensure all models are loaded
from app.db.base import Base
from app.models.product import Product, ProductCategory
from app.schemas.product import ProductCreate, ProductUpdate, ProductCategoryCreate, ProductCategoryUpdate


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    # Category methods
    def get_categories(self, skip: int = 0, limit: int = 100) -> List[ProductCategory]:
        """Get all active categories"""
        return self.db.query(ProductCategory).filter(
            ProductCategory.is_active == True
        ).offset(skip).limit(limit).all()

    def get_category_by_id(self, category_id: int) -> Optional[ProductCategory]:
        """Get category by ID"""
        return self.db.query(ProductCategory).filter(
            ProductCategory.id == category_id,
            ProductCategory.is_active == True
        ).first()

    def create_category(self, category_data: ProductCategoryCreate) -> ProductCategory:
        """Create a new product category"""
        # Generate slug if not provided
        slug = category_data.slug if category_data.slug else slugify(category_data.name)
        
        category = ProductCategory(
            name=category_data.name,
            description=category_data.description,
            slug=slug
        )
        
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    # Product methods
    def get_products(
        self,
        skip: int = 0,
        limit: int = 20,
        category_id: Optional[int] = None,
        is_featured: Optional[bool] = None,
        is_free: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Product]:
        """Get products with filtering"""
        query = self.db.query(Product).filter(Product.is_active == True)
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        if is_featured is not None:
            query = query.filter(Product.is_featured == is_featured)
        
        if is_free is not None:
            query = query.filter(Product.is_free == is_free)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                    Product.short_description.ilike(search_term)
                )
            )
        
        return query.order_by(Product.created_at.desc()).offset(skip).limit(limit).all()

    def get_featured_products(self, limit: int = 10) -> List[Product]:
        """Get featured products"""
        return self.db.query(Product).filter(
            and_(Product.is_active == True, Product.is_featured == True)
        ).order_by(Product.created_at.desc()).limit(limit).all()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.db.query(Product).filter(
            and_(Product.id == product_id, Product.is_active == True)
        ).first()

    def get_product_by_slug(self, slug: str) -> Optional[Product]:
        """Get product by slug"""
        return self.db.query(Product).filter(
            and_(Product.slug == slug, Product.is_active == True)
        ).first()

    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product"""
        # Generate slug if not provided
        slug = product_data.slug if product_data.slug else slugify(product_data.name)
        
        product = Product(
            name=product_data.name,
            description=product_data.description,
            short_description=product_data.short_description,
            slug=slug,
            price=product_data.price,
            original_price=product_data.original_price,
            is_free=product_data.is_free,
            category_id=product_data.category_id
        )
        
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """Update a product"""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None

        update_data = product_data.model_dump(exclude_unset=True)
        
        # Update slug if name is changed
        if 'name' in update_data and not update_data.get('slug'):
            update_data['slug'] = slugify(update_data['name'])

        for field, value in update_data.items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int) -> bool:
        """Soft delete a product"""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False

        product.is_active = False
        self.db.commit()
        return True

    def increment_view_count(self, product_id: int) -> bool:
        """Increment product view count"""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False

        product.view_count += 1
        self.db.commit()
        return True

    def increment_purchase_count(self, product_id: int) -> bool:
        """Increment product purchase count"""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False

        product.purchase_count += 1
        self.db.commit()
        return True
