"""Модуль с ORM моделями базы данных (SQLAlchemy)."""

# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Institution(Base):
    """Модель учебного заведения."""

    __tablename__ = "institutions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    faculties = relationship(
        "Faculty", back_populates="institution", cascade="all, delete"
    )


class Faculty(Base):
    """Модель факультета."""

    __tablename__ = "faculties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"))
    institution = relationship("Institution", back_populates="faculties")
    teachers = relationship("Teacher", back_populates="faculty")
    students = relationship("Student", back_populates="faculty")


class Teacher(Base):
    """Модель преподавателя."""

    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("Faculty", back_populates="teachers")
    courses = relationship("Course", back_populates="teacher")


class Student(Base):
    """Модель студента."""

    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("Faculty", back_populates="students")


class Course(Base):
    """Модель учебного курса/предмета."""

    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="courses")
