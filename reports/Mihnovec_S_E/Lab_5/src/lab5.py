"""
Приложение для управления отделом кадров.
Реализовано с использованием FastAPI и SQLAlchemy.
"""

from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, ConfigDict

SQLALCHEMY_DATABASE_URL = "sqlite:///./hr_department.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# pylint: disable=too-few-public-methods
class Department(Base):
    """Модель таблицы отделов."""

    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="department")


class Position(Base):
    """Модель таблицы должностей."""

    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    salary = Column(Float)
    employees = relationship("Employee", back_populates="position")


class Employee(Base):
    """Модель таблицы сотрудников."""

    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))

    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")


class Project(Base):
    """Модель таблицы проектов."""

    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    budget = Column(Float)


class Assignment(Base):
    """Связующая таблица для сотрудников и проектов."""

    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    role = Column(String)


Base.metadata.create_all(bind=engine)


class DepartmentBase(BaseModel):
    """Базовая схема отдела."""

    name: str


class DepartmentCreate(DepartmentBase):
    """Схема для создания отдела."""


class DepartmentRead(DepartmentBase):
    """Схема для чтения отдела."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class EmployeeBase(BaseModel):
    """Базовая схема сотрудника."""

    first_name: str
    last_name: str
    email: str
    department_id: int
    position_id: int


class EmployeeCreate(EmployeeBase):
    """Схема для создания сотрудника."""


class EmployeeRead(EmployeeBase):
    """Схема для чтения сотрудника."""

    id: int
    model_config = ConfigDict(from_attributes=True)


def get_db():
    """Инициализация сессии БД."""
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="HR Management System API")


@app.post("/departments/", response_model=DepartmentRead)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    """Создать новый отдел."""
    db_dept = Department(name=dept.name)
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept


@app.get("/departments/", response_model=List[DepartmentRead])
def read_departments(db: Session = Depends(get_db)):
    """Получить список всех отделов."""
    return db.query(Department).all()


@app.post("/employees/", response_model=EmployeeRead)
def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    """Добавить нового сотрудника."""
    db_emp = Employee(**emp.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp


@app.get("/employees/{emp_id}", response_model=EmployeeRead)
def read_employee(emp_id: int, db: Session = Depends(get_db)):
    """Получить информацию о сотруднике по ID."""
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp


@app.put("/employees/{emp_id}", response_model=EmployeeRead)
def update_employee(emp_id: int, emp_data: EmployeeCreate, db: Session = Depends(get_db)):
    """Обновить данные сотрудника."""
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in emp_data.model_dump().items():
        setattr(db_emp, key, value)

    db.commit()
    db.refresh(db_emp)
    return db_emp


@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    """Удалить сотрудника."""
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_emp)
    db.commit()
    return {"detail": "Employee deleted successfully"}


@app.get("/")
def read_root():
    """Корневой эндпойнт для проверки работоспособности."""
    return {"message": "Система Отдела Кадров API работает. Перейдите на /docs для тестирования."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
