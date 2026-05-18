from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"

    d_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    sex = Column(String(1), nullable=False)
    nick_name = Column(String(50))
    phone = Column(String(20))
    email = Column(String(30))

    orders = relationship("Order", back_populates="client")


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    man_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    establish_date = Column(Date, nullable=False)

    products = relationship("Product", back_populates="manufacturer")


class Product(Base):
    __tablename__ = "products"

    pr_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(DECIMAL(15, 2), nullable=False)
    man_id = Column(Integer, ForeignKey("manufacturers.man_id"), nullable=False)

    manufacturer = relationship("Manufacturer", back_populates="products")
    order_items = relationship("OrdersSummary", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    ord_id = Column(Integer, primary_key=True)
    d_id = Column(Integer, ForeignKey("clients.d_id"), nullable=False)
    date_of_order = Column(Date, nullable=False)
    total_sum = Column(DECIMAL(15, 2), default=0.00)

    client = relationship("Client", back_populates="orders")
    items = relationship("OrdersSummary", back_populates="order")


class OrdersSummary(Base):
    __tablename__ = "orders_summary"

    ord_s_id = Column(Integer, primary_key=True)
    ord_id = Column(Integer, ForeignKey("orders.ord_id"), nullable=False)
    pr_id = Column(Integer, ForeignKey("products.pr_id"), nullable=False)
    count = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Computer(Base):
    __tablename__ = "computers"

    comp_id = Column(Integer, primary_key=True)
    serial_number = Column(String(50), nullable=False, unique=True)
    model = Column(String(100), nullable=False)
    processor = Column(String(100))
    ram_gb = Column(Integer)
    storage_gb = Column(Integer)
    status = Column(String(20), default="available")
    pr_id = Column(Integer, ForeignKey("products.pr_id"), nullable=False)

    product = relationship("Product")


engine = create_engine("sqlite:///computer_lab.db", echo=True)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
