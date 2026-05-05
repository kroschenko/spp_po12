"""CRUD helpers for the computer firm database."""

from __future__ import annotations

from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from . import models, schemas


def get_all_customers(database: Session) -> list[models.Customer]:
    """Return all customers."""
    statement = select(models.Customer).order_by(models.Customer.id)
    return list(database.scalars(statement))


def get_customer_or_404(database: Session, customer_id: int) -> models.Customer:
    """Return a single customer or raise 404."""
    customer = database.get(models.Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return customer


def create_customer(
    database: Session, payload: schemas.CustomerCreate
) -> models.Customer:
    """Create a customer."""
    customer = models.Customer(**payload.model_dump())
    database.add(customer)
    database.commit()
    database.refresh(customer)
    return customer


def update_customer(
    database: Session, customer_id: int, payload: schemas.CustomerUpdate
) -> models.Customer:
    """Update an existing customer."""
    customer = get_customer_or_404(database, customer_id)
    for field_name, value in payload.model_dump().items():
        setattr(customer, field_name, value)
    database.commit()
    database.refresh(customer)
    return customer


def delete_customer(database: Session, customer_id: int) -> None:
    """Delete a customer."""
    customer = get_customer_or_404(database, customer_id)
    if customer.orders:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить клиента, у которого есть заказы",
        )
    database.delete(customer)
    database.commit()


def get_all_employees(database: Session) -> list[models.Employee]:
    """Return all employees."""
    statement = select(models.Employee).order_by(models.Employee.id)
    return list(database.scalars(statement))


def get_employee_or_404(database: Session, employee_id: int) -> models.Employee:
    """Return a single employee or raise 404."""
    employee = database.get(models.Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return employee


def create_employee(
    database: Session, payload: schemas.EmployeeCreate
) -> models.Employee:
    """Create an employee."""
    employee = models.Employee(**payload.model_dump())
    database.add(employee)
    database.commit()
    database.refresh(employee)
    return employee


def update_employee(
    database: Session, employee_id: int, payload: schemas.EmployeeUpdate
) -> models.Employee:
    """Update an employee."""
    employee = get_employee_or_404(database, employee_id)
    for field_name, value in payload.model_dump().items():
        setattr(employee, field_name, value)
    database.commit()
    database.refresh(employee)
    return employee


def delete_employee(database: Session, employee_id: int) -> None:
    """Delete an employee."""
    employee = get_employee_or_404(database, employee_id)
    if employee.orders:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить сотрудника, который привязан к заказам",
        )
    database.delete(employee)
    database.commit()


def get_all_suppliers(database: Session) -> list[models.Supplier]:
    """Return all suppliers."""
    statement = select(models.Supplier).order_by(models.Supplier.id)
    return list(database.scalars(statement))


def get_supplier_or_404(database: Session, supplier_id: int) -> models.Supplier:
    """Return a single supplier or raise 404."""
    supplier = database.get(models.Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Поставщик не найден")
    return supplier


def create_supplier(
    database: Session, payload: schemas.SupplierCreate
) -> models.Supplier:
    """Create a supplier."""
    supplier = models.Supplier(**payload.model_dump())
    database.add(supplier)
    database.commit()
    database.refresh(supplier)
    return supplier


def update_supplier(
    database: Session, supplier_id: int, payload: schemas.SupplierUpdate
) -> models.Supplier:
    """Update a supplier."""
    supplier = get_supplier_or_404(database, supplier_id)
    for field_name, value in payload.model_dump().items():
        setattr(supplier, field_name, value)
    database.commit()
    database.refresh(supplier)
    return supplier


def delete_supplier(database: Session, supplier_id: int) -> None:
    """Delete a supplier."""
    supplier = get_supplier_or_404(database, supplier_id)
    if supplier.products:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить поставщика, у которого есть товары",
        )
    database.delete(supplier)
    database.commit()


def get_all_categories(database: Session) -> list[models.Category]:
    """Return all categories."""
    statement = select(models.Category).order_by(models.Category.id)
    return list(database.scalars(statement))


def get_category_or_404(database: Session, category_id: int) -> models.Category:
    """Return a single category or raise 404."""
    category = database.get(models.Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


def create_category(
    database: Session, payload: schemas.CategoryCreate
) -> models.Category:
    """Create a category."""
    category = models.Category(**payload.model_dump())
    database.add(category)
    database.commit()
    database.refresh(category)
    return category


def update_category(
    database: Session, category_id: int, payload: schemas.CategoryUpdate
) -> models.Category:
    """Update a category."""
    category = get_category_or_404(database, category_id)
    for field_name, value in payload.model_dump().items():
        setattr(category, field_name, value)
    database.commit()
    database.refresh(category)
    return category


def delete_category(database: Session, category_id: int) -> None:
    """Delete a category."""
    category = get_category_or_404(database, category_id)
    if category.products:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить категорию, у которой есть товары",
        )
    database.delete(category)
    database.commit()


def get_all_products(database: Session) -> list[models.Product]:
    """Return all products."""
    statement = select(models.Product).order_by(models.Product.id)
    return list(database.scalars(statement))


def get_product_or_404(database: Session, product_id: int) -> models.Product:
    """Return a single product or raise 404."""
    product = database.get(models.Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


def ensure_related_entities_exist(
    database: Session, category_id: int, supplier_id: int
) -> None:
    """Validate that supplier and category exist."""
    if database.get(models.Category, category_id) is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    if database.get(models.Supplier, supplier_id) is None:
        raise HTTPException(status_code=404, detail="Поставщик не найден")


def create_product(database: Session, payload: schemas.ProductCreate) -> models.Product:
    """Create a product."""
    ensure_related_entities_exist(database, payload.category_id, payload.supplier_id)
    product = models.Product(**payload.model_dump())
    database.add(product)
    database.commit()
    database.refresh(product)
    return product


def update_product(
    database: Session, product_id: int, payload: schemas.ProductUpdate
) -> models.Product:
    """Update a product."""
    ensure_related_entities_exist(database, payload.category_id, payload.supplier_id)
    product = get_product_or_404(database, product_id)
    for field_name, value in payload.model_dump().items():
        setattr(product, field_name, value)
    database.commit()
    database.refresh(product)
    return product


def delete_product(database: Session, product_id: int) -> None:
    """Delete a product."""
    product = get_product_or_404(database, product_id)
    if product.order_items:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить товар, который уже есть в заказах",
        )
    database.delete(product)
    database.commit()


def get_all_orders(database: Session) -> list[models.Order]:
    """Return all orders with items."""
    statement = (
        select(models.Order)
        .options(joinedload(models.Order.items))
        .order_by(models.Order.id)
    )
    return list(database.scalars(statement).unique())


def get_order_or_404(database: Session, order_id: int) -> models.Order:
    """Return a single order with items or raise 404."""
    statement = (
        select(models.Order)
        .where(models.Order.id == order_id)
        .options(joinedload(models.Order.items))
    )
    order = database.scalars(statement).unique().one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


def validate_order_links(database: Session, customer_id: int, employee_id: int) -> None:
    """Validate that customer and employee exist."""
    if database.get(models.Customer, customer_id) is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    if database.get(models.Employee, employee_id) is None:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")


def create_order(database: Session, payload: schemas.OrderCreate) -> models.Order:
    """Create an order with order items."""
    validate_order_links(database, payload.customer_id, payload.employee_id)

    order = models.Order(
        customer_id=payload.customer_id,
        employee_id=payload.employee_id,
        order_date=payload.order_date,
        status=payload.status,
        total_amount=Decimal("0.00"),
    )

    total_amount = Decimal("0.00")
    for item_payload in payload.items:
        product = get_product_or_404(database, item_payload.product_id)
        if product.stock_quantity < item_payload.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара на складе: {product.name}",
            )
        product.stock_quantity -= item_payload.quantity
        total_amount += Decimal(product.price) * item_payload.quantity
        order.items.append(
            models.OrderItem(
                product_id=product.id,
                quantity=item_payload.quantity,
                unit_price=product.price,
            )
        )

    order.total_amount = total_amount
    database.add(order)
    database.commit()
    database.refresh(order)
    return get_order_or_404(database, order.id)


def update_order_status(
    database: Session, order_id: int, payload: schemas.OrderStatusUpdate
) -> models.Order:
    """Update order status."""
    order = get_order_or_404(database, order_id)
    order.status = payload.status
    database.commit()
    database.refresh(order)
    return get_order_or_404(database, order.id)


def delete_order(database: Session, order_id: int) -> None:
    """Delete an order and restore stock."""
    order = get_order_or_404(database, order_id)
    for item in order.items:
        product = get_product_or_404(database, item.product_id)
        product.stock_quantity += item.quantity
    database.delete(order)
    database.commit()
