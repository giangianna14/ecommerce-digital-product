from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.core.database import Base


class OrderStatus(PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    
    # User relationship
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="orders")
    
    # Order details
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Customer information
    customer_email = Column(String(255), nullable=False)
    customer_name = Column(String(255), nullable=False)
    
    # Payment information
    payment_method = Column(String(50), nullable=True)
    payment_status = Column(String(50), nullable=True)
    payment_intent_id = Column(String(255), nullable=True)  # Stripe payment intent ID
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order")
    
    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}', status='{self.status}')>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    
    # Order relationship
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="order_items")
    
    # Product relationship
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product", back_populates="order_items")
    
    # Item details
    product_name = Column(String(255), nullable=False)  # Snapshot of product name
    product_price = Column(DECIMAL(10, 2), nullable=False)  # Snapshot of product price
    quantity = Column(Integer, default=1, nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    
    # Download tracking
    download_count = Column(Integer, default=0)
    download_limit = Column(Integer, default=5)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    first_downloaded_at = Column(DateTime(timezone=True), nullable=True)
    last_downloaded_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_name='{self.product_name}', quantity={self.quantity})>"
