"""CRUD operations for rental service."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

import models
import schemas


class CustomerCRUD:
    """CRUD operations for customers."""

    @staticmethod
    def create(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
        """Create new customer."""
        db_customer = models.Customer(**customer.model_dump())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
        """Get all customers."""
        return db.query(models.Customer).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, customer_id: int) -> Optional[models.Customer]:
        """Get customer by ID."""
        return (
            db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        )

    @staticmethod
    def update(
        db: Session, customer_id: int, customer_data: schemas.CustomerCreate
    ) -> Optional[models.Customer]:
        """Update customer."""
        db_customer = CustomerCRUD.get_by_id(db, customer_id)
        if not db_customer:
            return None
        for key, value in customer_data.model_dump().items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
        return db_customer

    @staticmethod
    def delete(db: Session, customer_id: int) -> bool:
        """Delete customer."""
        db_customer = CustomerCRUD.get_by_id(db, customer_id)
        if not db_customer:
            return False
        db.delete(db_customer)
        db.commit()
        return True


class ProductCategoryCRUD:
    """CRUD operations for product categories."""

    @staticmethod
    def create(
        db: Session, category: schemas.ProductCategoryCreate
    ) -> models.ProductCategory:
        """Create new product category."""
        db_category = models.ProductCategory(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def get_all(db: Session) -> List[models.ProductCategory]:
        """Get all product categories."""
        return db.query(models.ProductCategory).all()

    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Optional[models.ProductCategory]:
        """Get category by ID."""
        return (
            db.query(models.ProductCategory)
            .filter(models.ProductCategory.id == category_id)
            .first()
        )


class ProductCRUD:
    """CRUD operations for products."""

    @staticmethod
    def create(db: Session, product: schemas.ProductCreate) -> models.Product:
        """Create new product."""
        db_product = models.Product(
            **product.model_dump(), available_quantity=product.total_quantity
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def get_all(
        db: Session, skip: int = 0, limit: int = 100, available_only: bool = False
    ) -> List[models.Product]:
        """Get all products."""
        query = db.query(models.Product)
        if available_only:
            query = query.filter(models.Product.is_available is True)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Optional[models.Product]:
        """Get product by ID."""
        return db.query(models.Product).filter(models.Product.id == product_id).first()

    @staticmethod
    def update(
        db: Session, product_id: int, product_data: schemas.ProductCreate
    ) -> Optional[models.Product]:
        """Update product."""
        db_product = ProductCRUD.get_by_id(db, product_id)
        if not db_product:
            return None
        for key, value in product_data.model_dump().items():
            setattr(db_product, key, value)
        db_product.available_quantity = product_data.total_quantity
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def delete(db: Session, product_id: int) -> bool:
        """Delete product."""
        db_product = ProductCRUD.get_by_id(db, product_id)
        if not db_product:
            return False
        db.delete(db_product)
        db.commit()
        return True


class RentalCRUD:
    """CRUD operations for rentals."""

    @staticmethod
    def create(db: Session, rental: schemas.RentalCreate) -> Optional[models.Rental]:
        """Create new rental."""
        product = ProductCRUD.get_by_id(db, rental.product_id)
        if not product or product.available_quantity <= 0:
            return None

        db_rental = models.Rental(**rental.model_dump())
        db.add(db_rental)
        product.available_quantity -= 1
        if product.available_quantity == 0:
            product.is_available = False

        db.commit()
        db.refresh(db_rental)
        return db_rental

    @staticmethod
    def get_all(
        db: Session, skip: int = 0, limit: int = 100, customer_id: Optional[int] = None
    ) -> List[models.Rental]:
        """Get all rentals."""
        query = db.query(models.Rental)
        if customer_id:
            query = query.filter(models.Rental.customer_id == customer_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, rental_id: int) -> Optional[models.Rental]:
        """Get rental by ID."""
        return db.query(models.Rental).filter(models.Rental.id == rental_id).first()

    @staticmethod
    def return_product(db: Session, rental_id: int) -> Optional[models.Rental]:
        """Mark product as returned."""
        db_rental = RentalCRUD.get_by_id(db, rental_id)
        if not db_rental or db_rental.status != "active":
            return None

        db_rental.actual_return_date = datetime.now()
        db_rental.status = "returned"

        product = ProductCRUD.get_by_id(db, db_rental.product_id)
        if product:
            product.available_quantity += 1
            product.is_available = True

        db.commit()
        db.refresh(db_rental)
        return db_rental


class PaymentCRUD:
    """CRUD operations for payments."""

    @staticmethod
    def create(db: Session, payment: schemas.PaymentCreate) -> models.Payment:
        """Create new payment."""
        db_payment = models.Payment(**payment.model_dump())
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment

    @staticmethod
    def get_by_customer(
        db: Session, customer_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.Payment]:
        """Get payments by customer."""
        return (
            db.query(models.Payment)
            .filter(models.Payment.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
