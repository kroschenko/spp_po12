"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CustomerBase(BaseModel):
    """Base customer schema."""

    first_name: str
    last_name: str
    email: str
    phone: str
    address: Optional[str] = None
    passport_number: Optional[str] = None


class CustomerCreate(CustomerBase):
    """Customer creation schema."""


class CustomerResponse(CustomerBase):
    """Customer response schema."""

    id: int
    registration_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class ProductCategoryBase(BaseModel):
    """Base product category schema."""

    name: str
    description: Optional[str] = None


class ProductCategoryCreate(ProductCategoryBase):
    """Product category creation schema."""


class ProductCategoryResponse(ProductCategoryBase):
    """Product category response schema."""

    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    """Base product schema."""

    name: str
    description: Optional[str] = None
    category_id: int
    daily_price: float
    deposit_amount: float = 0.0
    total_quantity: int = 1


class ProductCreate(ProductBase):
    """Product creation schema."""


class ProductResponse(ProductBase):
    """Product response schema."""

    id: int
    available_quantity: int
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RentalBase(BaseModel):
    """Base rental schema."""

    customer_id: int
    product_id: int
    expected_return_date: datetime
    total_amount: float


class RentalCreate(RentalBase):
    """Rental creation schema."""


class RentalResponse(RentalBase):
    """Rental response schema."""

    id: int
    rental_date: datetime
    actual_return_date: Optional[datetime]
    deposit_paid: float
    status: str

    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    """Base payment schema."""

    customer_id: int
    rental_id: int
    amount: float
    payment_method: str


class PaymentCreate(PaymentBase):
    """Payment creation schema."""


class PaymentResponse(PaymentBase):
    """Payment response schema."""

    id: int
    payment_date: datetime
    status: str

    class Config:
        from_attributes = True
