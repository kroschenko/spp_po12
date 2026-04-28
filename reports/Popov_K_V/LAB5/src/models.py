"""
Модуль с описанием моделей таблиц базы данных для SQLAlchemy.
Содержит описание структуры таблиц: агентства, сотрудники, клиенты, туры и бронирования.
"""
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# pylint: disable=too-few-public-methods
# Это отключает предупреждение R0903, так как модели БД — это структуры данных,
# и им не обязательно иметь публичные методы.

class Agency(Base):
    """Модель таблицы агентств (филиалов)."""
    __tablename__ = "agencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    phone = Column(String(20))

    employees = relationship("Employee", back_populates="agency")


class Employee(Base):
    """Модель таблицы сотрудников агентства."""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    agency_id = Column(Integer, ForeignKey("agencies.id", ondelete="CASCADE"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    position = Column(String(50))

    agency = relationship("Agency", back_populates="employees")
    bookings = relationship("Booking", back_populates="employee")


class Client(Base):
    """Модель таблицы клиентов агентства."""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))

    bookings = relationship("Booking", back_populates="client")


class Tour(Base):
    """Модель таблицы доступных туров (путевок)."""
    __tablename__ = "tours"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    bookings = relationship("Booking", back_populates="tour")


class Booking(Base):
    """Модель таблицы бронирований, связывающая клиента, тур и сотрудника."""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    tour_id = Column(Integer, ForeignKey("tours.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    booking_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)

    client = relationship("Client", back_populates="bookings")
    tour = relationship("Tour", back_populates="bookings")
    employee = relationship("Employee", back_populates="bookings")
