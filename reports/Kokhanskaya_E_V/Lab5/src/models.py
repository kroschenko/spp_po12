"""Database models for rental service."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Customer(Base):
    """Customer model - people who rent items."""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(200))
    passport_number = Column(String(20), unique=True)
    registration_date = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)

    rentals = relationship("Rental", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")


class ProductCategory(Base):
    """Product category model."""

    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(200))

    products = relationship("Product", back_populates="category")


class Product(Base):
    """Product model - items available for rent."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    category_id = Column(Integer, ForeignKey("product_categories.id"))
    daily_price = Column(Float, nullable=False)
    deposit_amount = Column(Float, default=0.0)
    total_quantity = Column(Integer, default=1)
    available_quantity = Column(Integer, default=1)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    category = relationship("ProductCategory", back_populates="products")
    rentals = relationship("Rental", back_populates="product")


class Rental(Base):
    """Rental model - records of item rentals."""

    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    rental_date = Column(DateTime, default=datetime.now)
    expected_return_date = Column(DateTime, nullable=False)
    actual_return_date = Column(DateTime)
    total_amount = Column(Float, nullable=False)
    deposit_paid = Column(Float, default=0.0)
    status = Column(
        String(20), default="active"
    )  # active, returned, overdue, cancelled

    customer = relationship("Customer", back_populates="rentals")
    product = relationship("Product", back_populates="rentals")


class Payment(Base):
    """Payment model - records of customer payments."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    rental_id = Column(Integer, ForeignKey("rentals.id"))
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.now)
    payment_method = Column(String(30))  # cash, card, online
    status = Column(String(20), default="completed")

    customer = relationship("Customer", back_populates="payments")
