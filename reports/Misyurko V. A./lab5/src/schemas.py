"""Pydantic schemas for request and response bodies."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ORMBaseModel(BaseModel):
    """Base Pydantic model configured for ORM objects."""

    model_config = ConfigDict(from_attributes=True)


class CustomerBase(BaseModel):
    """Shared customer fields."""

    full_name: str = Field(min_length=3, max_length=120)
    email: str = Field(min_length=5, max_length=120)
    phone: str = Field(min_length=5, max_length=30)
    city: str = Field(min_length=2, max_length=80)


class CustomerCreate(CustomerBase):
    """Payload for customer creation."""


class CustomerUpdate(CustomerBase):
    """Payload for customer update."""


class CustomerRead(CustomerBase, ORMBaseModel):
    """Customer response."""

    id: int


class EmployeeBase(BaseModel):
    """Shared employee fields."""

    full_name: str = Field(min_length=3, max_length=120)
    position: str = Field(min_length=2, max_length=80)
    hire_date: date
    salary: Decimal = Field(gt=0)


class EmployeeCreate(EmployeeBase):
    """Payload for employee creation."""


class EmployeeUpdate(EmployeeBase):
    """Payload for employee update."""


class EmployeeRead(EmployeeBase, ORMBaseModel):
    """Employee response."""

    id: int


class SupplierBase(BaseModel):
    """Shared supplier fields."""

    name: str = Field(min_length=2, max_length=120)
    contact_email: str = Field(min_length=5, max_length=120)
    phone: str = Field(min_length=5, max_length=30)


class SupplierCreate(SupplierBase):
    """Payload for supplier creation."""


class SupplierUpdate(SupplierBase):
    """Payload for supplier update."""


class SupplierRead(SupplierBase, ORMBaseModel):
    """Supplier response."""

    id: int


class CategoryBase(BaseModel):
    """Shared category fields."""

    name: str = Field(min_length=2, max_length=80)
    description: str = Field(min_length=5)


class CategoryCreate(CategoryBase):
    """Payload for category creation."""


class CategoryUpdate(CategoryBase):
    """Payload for category update."""


class CategoryRead(CategoryBase, ORMBaseModel):
    """Category response."""

    id: int


class ProductBase(BaseModel):
    """Shared product fields."""

    name: str = Field(min_length=2, max_length=120)
    category_id: int = Field(gt=0)
    supplier_id: int = Field(gt=0)
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)


class ProductCreate(ProductBase):
    """Payload for product creation."""


class ProductUpdate(ProductBase):
    """Payload for product update."""


class ProductRead(ProductBase, ORMBaseModel):
    """Product response."""

    id: int


class OrderItemCreate(BaseModel):
    """Payload for order item creation."""

    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderItemRead(ORMBaseModel):
    """Order item response."""

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal


class OrderCreate(BaseModel):
    """Payload for order creation."""

    customer_id: int = Field(gt=0)
    employee_id: int = Field(gt=0)
    order_date: datetime
    status: str = Field(min_length=3, max_length=40)
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderStatusUpdate(BaseModel):
    """Payload for updating order status."""

    status: str = Field(min_length=3, max_length=40)


class OrderRead(ORMBaseModel):
    """Order response with items."""

    id: int
    customer_id: int
    employee_id: int
    order_date: datetime
    status: str
    total_amount: Decimal
    items: list[OrderItemRead]
