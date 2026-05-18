# pylint: disable=too-many-positional-arguments
from datetime import date
from sqlalchemy.orm import Session
from database import Client, Manufacturer, Product, Order, OrdersSummary, Computer


def create_client(db: Session, first_name, last_name, sex, nick_name=None, phone=None, email=None):
    client = Client(
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        nick_name=nick_name,
        phone=phone,
        email=email
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def get_clients(db: Session, skip=0, limit=100):
    return db.query(Client).offset(skip).limit(limit).all()


def get_client(db: Session, client_id):
    return db.query(Client).filter(Client.d_id == client_id).first()


def update_client(db: Session, client_id, **kwargs):
    client = db.query(Client).filter(Client.d_id == client_id).first()
    if client:
        for key, value in kwargs.items():
            if hasattr(client, key):
                setattr(client, key, value)
        db.commit()
        db.refresh(client)
    return client


def delete_client(db: Session, client_id):
    client = db.query(Client).filter(Client.d_id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
        return True
    return False


def create_product(db: Session, name, price, man_id):
    product = Product(name=name, price=price, man_id=man_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session, skip=0, limit=100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id):
    return db.query(Product).filter(Product.pr_id == product_id).first()


def update_product(db: Session, product_id, **kwargs):
    product = db.query(Product).filter(Product.pr_id == product_id).first()
    if product:
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product


def delete_product(db: Session, product_id):
    product = db.query(Product).filter(Product.pr_id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False


def create_order(db: Session, d_id, items):
    order = Order(d_id=d_id, date_of_order=date.today(), total_sum=0.00)
    db.add(order)
    db.flush()

    total = 0
    for item in items:
        product = db.query(Product).filter(Product.pr_id == item["pr_id"]).first()
        if product:
            order_item = OrdersSummary(
                ord_id=order.ord_id,
                pr_id=item["pr_id"],
                count=item["count"]
            )
            db.add(order_item)
            total += float(product.price) * item["count"]

    order.total_sum = total
    db.commit()
    db.refresh(order)
    return order


def get_orders(db: Session, skip=0, limit=100):
    return db.query(Order).offset(skip).limit(limit).all()


def get_order(db: Session, order_id):
    return db.query(Order).filter(Order.ord_id == order_id).first()


def update_order(db: Session, order_id, **kwargs):
    order = db.query(Order).filter(Order.ord_id == order_id).first()
    if order:
        for key, value in kwargs.items():
            if hasattr(order, key):
                setattr(order, key, value)
        db.commit()
        db.refresh(order)
    return order


def delete_order(db: Session, order_id):
    order = db.query(Order).filter(Order.ord_id == order_id).first()
    if order:
        db.query(OrdersSummary).filter(OrdersSummary.ord_id == order_id).delete()
        db.delete(order)
        db.commit()
        return True
    return False


def create_manufacturer(db: Session, name, establish_date):
    manufacturer = Manufacturer(name=name, establish_date=establish_date)
    db.add(manufacturer)
    db.commit()
    db.refresh(manufacturer)
    return manufacturer


def get_manufacturers(db: Session, skip=0, limit=100):
    return db.query(Manufacturer).offset(skip).limit(limit).all()


def get_manufacturer(db: Session, man_id):
    return db.query(Manufacturer).filter(Manufacturer.man_id == man_id).first()


def update_manufacturer(db: Session, man_id, **kwargs):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.man_id == man_id).first()
    if manufacturer:
        for key, value in kwargs.items():
            if hasattr(manufacturer, key):
                setattr(manufacturer, key, value)
        db.commit()
        db.refresh(manufacturer)
    return manufacturer


def delete_manufacturer(db: Session, man_id):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.man_id == man_id).first()
    if manufacturer:
        db.delete(manufacturer)
        db.commit()
        return True
    return False


def get_order_details(db: Session, order_id):
    result = db.query(
        Order.ord_id,
        Client.first_name,
        Client.last_name,
        Order.date_of_order,
        Order.total_sum,
        Product.name,
        OrdersSummary.count,
        (Product.price * OrdersSummary.count).label("subtotal")
    ).join(Client, Order.d_id == Client.d_id)\
     .join(OrdersSummary, Order.ord_id == OrdersSummary.ord_id)\
     .join(Product, OrdersSummary.pr_id == Product.pr_id)\
     .filter(Order.ord_id == order_id).all()
    return result


def create_computer(db: Session, serial_number, model, processor, ram_gb, storage_gb, pr_id, status="available"):
    computer = Computer(
        serial_number=serial_number,
        model=model,
        processor=processor,
        ram_gb=ram_gb,
        storage_gb=storage_gb,
        status=status,
        pr_id=pr_id
    )
    db.add(computer)
    db.commit()
    db.refresh(computer)
    return computer


def get_computers(db: Session, skip=0, limit=100):
    return db.query(Computer).offset(skip).limit(limit).all()


def get_computer(db: Session, comp_id):
    return db.query(Computer).filter(Computer.comp_id == comp_id).first()


def update_computer(db: Session, comp_id, **kwargs):
    computer = db.query(Computer).filter(Computer.comp_id == comp_id).first()
    if computer:
        for key, value in kwargs.items():
            if hasattr(computer, key):
                setattr(computer, key, value)
        db.commit()
        db.refresh(computer)
    return computer


def delete_computer(db: Session, comp_id):
    computer = db.query(Computer).filter(Computer.comp_id == comp_id).first()
    if computer:
        db.delete(computer)
        db.commit()
        return True
    return False
