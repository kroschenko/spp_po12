"""Модели базы данных SQLAlchemy для Лабораторной работы №5."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Group(Base):
    """Модель таблицы групп."""

    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    students = relationship("Student", back_populates="group")


class Student(Base):
    """Модель таблицы студентов."""

    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="students")
