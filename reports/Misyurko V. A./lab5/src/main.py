"""FastAPI application for the computer firm database."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Response, status
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import SESSION_LOCAL, get_db
from .seed import initialize_database


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Initialize the database on startup."""
    database = SESSION_LOCAL()
    try:
        initialize_database(database)
        yield
    finally:
        database.close()


app = FastAPI(
    title="Computer Firm API",
    description=(
        "CRUD API for a computer firm database built with SQLite " "and SQLAlchemy."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a short description of the API."""
    return {
        "message": "API базы данных 'Компьютерная фирма' работает",
        "docs": "/docs",
    }


@app.get("/customers", response_model=list[schemas.CustomerRead])
def read_customers(database: Session = Depends(get_db)) -> list[schemas.CustomerRead]:
    """Return all customers."""
    return crud.get_all_customers(database)


@app.post(
    "/customers",
    response_model=schemas.CustomerRead,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    payload: schemas.CustomerCreate, database: Session = Depends(get_db)
) -> schemas.CustomerRead:
    """Create a customer."""
    return crud.create_customer(database, payload)


@app.put("/customers/{customer_id}", response_model=schemas.CustomerRead)
def update_customer(
    customer_id: int,
    payload: schemas.CustomerUpdate,
    database: Session = Depends(get_db),
) -> schemas.CustomerRead:
    """Update a customer."""
    return crud.update_customer(database, customer_id, payload)


@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, database: Session = Depends(get_db)) -> Response:
    """Delete a customer."""
    crud.delete_customer(database, customer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/employees", response_model=list[schemas.EmployeeRead])
def read_employees(database: Session = Depends(get_db)) -> list[schemas.EmployeeRead]:
    """Return all employees."""
    return crud.get_all_employees(database)


@app.post(
    "/employees",
    response_model=schemas.EmployeeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    payload: schemas.EmployeeCreate, database: Session = Depends(get_db)
) -> schemas.EmployeeRead:
    """Create an employee."""
    return crud.create_employee(database, payload)


@app.put("/employees/{employee_id}", response_model=schemas.EmployeeRead)
def update_employee(
    employee_id: int,
    payload: schemas.EmployeeUpdate,
    database: Session = Depends(get_db),
) -> schemas.EmployeeRead:
    """Update an employee."""
    return crud.update_employee(database, employee_id, payload)


@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, database: Session = Depends(get_db)) -> Response:
    """Delete an employee."""
    crud.delete_employee(database, employee_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/suppliers", response_model=list[schemas.SupplierRead])
def read_suppliers(database: Session = Depends(get_db)) -> list[schemas.SupplierRead]:
    """Return all suppliers."""
    return crud.get_all_suppliers(database)


@app.post(
    "/suppliers",
    response_model=schemas.SupplierRead,
    status_code=status.HTTP_201_CREATED,
)
def create_supplier(
    payload: schemas.SupplierCreate, database: Session = Depends(get_db)
) -> schemas.SupplierRead:
    """Create a supplier."""
    return crud.create_supplier(database, payload)


@app.put("/suppliers/{supplier_id}", response_model=schemas.SupplierRead)
def update_supplier(
    supplier_id: int,
    payload: schemas.SupplierUpdate,
    database: Session = Depends(get_db),
) -> schemas.SupplierRead:
    """Update a supplier."""
    return crud.update_supplier(database, supplier_id, payload)


@app.delete("/suppliers/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, database: Session = Depends(get_db)) -> Response:
    """Delete a supplier."""
    crud.delete_supplier(database, supplier_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/categories", response_model=list[schemas.CategoryRead])
def read_categories(database: Session = Depends(get_db)) -> list[schemas.CategoryRead]:
    """Return all categories."""
    return crud.get_all_categories(database)


@app.post(
    "/categories",
    response_model=schemas.CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    payload: schemas.CategoryCreate, database: Session = Depends(get_db)
) -> schemas.CategoryRead:
    """Create a category."""
    return crud.create_category(database, payload)


@app.put("/categories/{category_id}", response_model=schemas.CategoryRead)
def update_category(
    category_id: int,
    payload: schemas.CategoryUpdate,
    database: Session = Depends(get_db),
) -> schemas.CategoryRead:
    """Update a category."""
    return crud.update_category(database, category_id, payload)


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, database: Session = Depends(get_db)) -> Response:
    """Delete a category."""
    crud.delete_category(database, category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/products", response_model=list[schemas.ProductRead])
def read_products(database: Session = Depends(get_db)) -> list[schemas.ProductRead]:
    """Return all products."""
    return crud.get_all_products(database)


@app.post(
    "/products",
    response_model=schemas.ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: schemas.ProductCreate, database: Session = Depends(get_db)
) -> schemas.ProductRead:
    """Create a product."""
    return crud.create_product(database, payload)


@app.put("/products/{product_id}", response_model=schemas.ProductRead)
def update_product(
    product_id: int,
    payload: schemas.ProductUpdate,
    database: Session = Depends(get_db),
) -> schemas.ProductRead:
    """Update a product."""
    return crud.update_product(database, product_id, payload)


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, database: Session = Depends(get_db)) -> Response:
    """Delete a product."""
    crud.delete_product(database, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/orders", response_model=list[schemas.OrderRead])
def read_orders(database: Session = Depends(get_db)) -> list[schemas.OrderRead]:
    """Return all orders."""
    return crud.get_all_orders(database)


@app.post(
    "/orders",
    response_model=schemas.OrderRead,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    payload: schemas.OrderCreate, database: Session = Depends(get_db)
) -> schemas.OrderRead:
    """Create an order."""
    return crud.create_order(database, payload)


@app.put("/orders/{order_id}", response_model=schemas.OrderRead)
def update_order(
    order_id: int,
    payload: schemas.OrderStatusUpdate,
    database: Session = Depends(get_db),
) -> schemas.OrderRead:
    """Update order status."""
    return crud.update_order_status(database, order_id, payload)


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, database: Session = Depends(get_db)) -> Response:
    """Delete an order."""
    crud.delete_order(database, order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
