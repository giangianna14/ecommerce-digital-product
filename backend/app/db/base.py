# Import all models here for Alembic
from app.models.user import User
from app.models.product import Product, ProductCategory
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.core.database import Base

# This ensures all models are imported when Alembic runs
