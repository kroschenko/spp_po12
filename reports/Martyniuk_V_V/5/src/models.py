"""Модели таблиц базы данных."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Group(Base):
    """Модель группы студентов."""

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    students = relationship(
        "Student", back_populates="group", cascade="all, delete-orphan"
    )


class Student(Base):
    """Модель студента."""

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))

    group = relationship("Group", back_populates="students")
    grades = relationship(
        "Grade", back_populates="student", cascade="all, delete-orphan"
    )


class Teacher(Base):
    """Модель преподавателя."""

    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    """Модель учебного предмета."""

    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"))

    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship(
        "Grade", back_populates="subject", cascade="all, delete-orphan"
    )


class Grade(Base):
    """Модель оценки студента."""

    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.now)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
