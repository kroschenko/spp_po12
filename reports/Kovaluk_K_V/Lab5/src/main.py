from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import date

from database import get_db, engine, Base
import crud

app = FastAPI(title="Computer Laboratory API")

Base.metadata.create_all(bind=engine)

class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    sex: str
    nick_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class ClientResponse(BaseModel):
    d_id: int
    first_name: str
    last_name: str
    sex: str
    nick_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class ProductCreate(BaseModel):
    name: str
    price: float
    man_id: int

class ProductResponse(BaseModel):
    pr_id: int
    name: str
    price: float
    man_id: int

class OrderItem(BaseModel):
    pr_id: int
    count: int

class OrderCreate(BaseModel):
    d_id: int
    items: List[OrderItem]

class OrderResponse(BaseModel):
    ord_id: int
    d_id: int
    date_of_order: date
    total_sum: float

class ManufacturerCreate(BaseModel):
    name: str
    establish_date: date

class ManufacturerResponse(BaseModel):
    man_id: int
    name: str
    establish_date: date

class ComputerCreate(BaseModel):
    serial_number: str
    model: str
    processor: Optional[str] = None
    ram_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    pr_id: int
    status: Optional[str] = "available"

class ComputerResponse(BaseModel):
    comp_id: int
    serial_number: str
    model: str
    processor: Optional[str] = None
    ram_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    status: str
    pr_id: int

@app.get("/")
def read_root():
    return {"message": "Computer Laboratory API"}

@app.post("/clients/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(
        db=db,
        first_name=client.first_name,
        last_name=client.last_name,
        sex=client.sex,
        nick_name=client.nick_name,
        phone=client.phone,
        email=client.email
    )

@app.get("/clients/", response_model=List[ClientResponse])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients

@app.get("/clients/{client_id}", response_model=ClientResponse)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/clients/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client: ClientCreate, db: Session = Depends(get_db)):
    updated = crud.update_client(
        db=db,
        client_id=client_id,
        first_name=client.first_name,
        last_name=client.last_name,
        sex=client.sex,
        nick_name=client.nick_name,
        phone=client.phone,
        email=client.email
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated

@app.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    success = crud.delete_client(db, client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}

@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, name=product.name, price=product.price, man_id=product.man_id)

@app.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(
        db=db,
        product_id=product_id,
        name=product.name,
        price=product.price,
        man_id=product.man_id
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    items = [{"pr_id": item.pr_id, "count": item.count} for item in order.items]
    return crud.create_order(db=db, d_id=order.d_id, items=items)

@app.get("/orders/", response_model=List[OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    success = crud.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

@app.post("/manufacturers/", response_model=ManufacturerResponse)
def create_manufacturer(manufacturer: ManufacturerCreate, db: Session = Depends(get_db)):
    return crud.create_manufacturer(db=db, name=manufacturer.name, establish_date=manufacturer.establish_date)

@app.get("/manufacturers/", response_model=List[ManufacturerResponse])
def read_manufacturers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    manufacturers = crud.get_manufacturers(db, skip=skip, limit=limit)
    return manufacturers

@app.get("/manufacturers/{man_id}", response_model=ManufacturerResponse)
def read_manufacturer(man_id: int, db: Session = Depends(get_db)):
    manufacturer = crud.get_manufacturer(db, man_id)
    if manufacturer is None:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return manufacturer

@app.put("/manufacturers/{man_id}", response_model=ManufacturerResponse)
def update_manufacturer(man_id: int, manufacturer: ManufacturerCreate, db: Session = Depends(get_db)):
    updated = crud.update_manufacturer(
        db=db,
        man_id=man_id,
        name=manufacturer.name,
        establish_date=manufacturer.establish_date
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return updated

@app.delete("/manufacturers/{man_id}")
def delete_manufacturer(man_id: int, db: Session = Depends(get_db)):
    success = crud.delete_manufacturer(db, man_id)
    if not success:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return {"message": "Manufacturer deleted successfully"}

@app.get("/orders/{order_id}/details")
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    details = crud.get_order_details(db, order_id)
    if not details:
        raise HTTPException(status_code=404, detail="Order not found")
    return details

@app.post("/computers/", response_model=ComputerResponse)
def create_computer(computer: ComputerCreate, db: Session = Depends(get_db)):
    return crud.create_computer(
        db=db,
        serial_number=computer.serial_number,
        model=computer.model,
        processor=computer.processor,
        ram_gb=computer.ram_gb,
        storage_gb=computer.storage_gb,
        pr_id=computer.pr_id,
        status=computer.status
    )

@app.get("/computers/", response_model=List[ComputerResponse])
def read_computers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    computers = crud.get_computers(db, skip=skip, limit=limit)
    return computers

@app.get("/computers/{comp_id}", response_model=ComputerResponse)
def read_computer(comp_id: int, db: Session = Depends(get_db)):
    computer = crud.get_computer(db, comp_id)
    if computer is None:
        raise HTTPException(status_code=404, detail="Computer not found")
    return computer

@app.put("/computers/{comp_id}", response_model=ComputerResponse)
def update_computer(comp_id: int, computer: ComputerCreate, db: Session = Depends(get_db)):
    updated = crud.update_computer(
        db=db,
        comp_id=comp_id,
        serial_number=computer.serial_number,
        model=computer.model,
        processor=computer.processor,
        ram_gb=computer.ram_gb,
        storage_gb=computer.storage_gb,
        pr_id=computer.pr_id,
        status=computer.status
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Computer not found")
    return updated

@app.delete("/computers/{comp_id}")
def delete_computer(comp_id: int, db: Session = Depends(get_db)):
    success = crud.delete_computer(db, comp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Computer not found")
    return {"message": "Computer deleted successfully"}
