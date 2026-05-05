"""Database initialization and demo data."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from .database import Base, engine
from .models import Category, Customer, Employee, Order, OrderItem, Product, Supplier


def create_tables() -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def seed_database(database: Session) -> None:
    """Fill the database with demo records on first start."""
    if database.query(Customer).first() is not None:
        return

    customers = [
        Customer(
            full_name="Иван Петров",
            email="ivan.petrov@example.com",
            phone="+375291111111",
            city="Минск",
        ),
        Customer(
            full_name="Анна Кузнецова",
            email="anna.k@example.com",
            phone="+375292222222",
            city="Гомель",
        ),
    ]
    employees = [
        Employee(
            full_name="Алексей Смирнов",
            position="Менеджер по продажам",
            hire_date=date(2023, 5, 10),
            salary=Decimal("1800.00"),
        ),
        Employee(
            full_name="Мария Соколова",
            position="Старший менеджер",
            hire_date=date(2022, 9, 1),
            salary=Decimal("2200.00"),
        ),
    ]
    suppliers = [
        Supplier(
            name="TechSupply",
            contact_email="sales@techsupply.by",
            phone="+375293333333",
        ),
        Supplier(
            name="Global Parts",
            contact_email="contact@globalparts.by",
            phone="+375294444444",
        ),
    ]
    categories = [
        Category(name="Ноутбуки", description="Портативные компьютеры"),
        Category(name="Комплектующие", description="Процессоры, видеокарты, SSD"),
        Category(name="Периферия", description="Клавиатуры, мыши, мониторы"),
    ]

    database.add_all(customers + employees + suppliers + categories)
    database.flush()

    products = [
        Product(
            name="Lenovo ThinkBook 15",
            category_id=categories[0].id,
            supplier_id=suppliers[0].id,
            price=Decimal("2450.00"),
            stock_quantity=7,
        ),
        Product(
            name="Samsung SSD 1TB",
            category_id=categories[1].id,
            supplier_id=suppliers[1].id,
            price=Decimal("320.00"),
            stock_quantity=25,
        ),
        Product(
            name="Logitech MX Master 3S",
            category_id=categories[2].id,
            supplier_id=suppliers[0].id,
            price=Decimal("410.00"),
            stock_quantity=14,
        ),
    ]
    database.add_all(products)
    database.flush()

    order = Order(
        customer_id=customers[0].id,
        employee_id=employees[0].id,
        order_date=datetime(2026, 3, 17, 10, 30),
        status="Создан",
        total_amount=Decimal("2770.00"),
    )
    database.add(order)
    database.flush()

    database.add_all(
        [
            OrderItem(
                order_id=order.id,
                product_id=products[0].id,
                quantity=1,
                unit_price=products[0].price,
            ),
            OrderItem(
                order_id=order.id,
                product_id=products[1].id,
                quantity=1,
                unit_price=products[1].price,
            ),
        ]
    )

    products[0].stock_quantity -= 1
    products[1].stock_quantity -= 1
    database.commit()


def initialize_database(database: Session) -> None:
    """Create tables and insert demo data."""
    create_tables()
    seed_database(database)
