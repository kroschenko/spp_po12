"""Модуль для работы с базой данных комплектующих ПК через SQLAlchemy."""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./computer_build.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Category(Base):  # pylint: disable=R0903
    """Класс для представления категории комплектующих."""

    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    components = relationship("Component", back_populates="category")


class Manufacturer(Base):  # pylint: disable=R0903
    """Класс для представления производителя комплектующих."""

    __tablename__ = "manufacturers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    components = relationship("Component", back_populates="manufacturer")


class Component(Base):  # pylint: disable=R0903
    """Класс для представления комплектующего ПК."""

    __tablename__ = "components"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))

    category = relationship("Category", back_populates="components")
    manufacturer = relationship("Manufacturer", back_populates="components")


class Order(Base):  # pylint: disable=R0903
    """Класс для представления заказа на сборку ПК."""

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    total_price = Column(Float, default=0.0)


class OrderItem(Base):  # pylint: disable=R0903
    """Класс для представления элемента заказа."""

    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    component_id = Column(Integer, ForeignKey("components.id"))
    quantity = Column(Integer, default=1)

    order = relationship("Order", backref="items")
    component = relationship("Component")


Base.metadata.create_all(bind=engine)
