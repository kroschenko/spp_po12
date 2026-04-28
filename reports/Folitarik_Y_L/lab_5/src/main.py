"""
Модуль для управления системой проката DVD-дисков.

Реализует API с использованием FastAPI, SQLAlchemy (SQLite) и Pydantic.
Код соответствует стандартам Pylint: содержит документацию всех сущностей
и правильное именование компонентов.
"""

from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    Session,
    relationship,
)
from pydantic import BaseModel, ConfigDict

# --- Константы и настройки базы данных ---
DATABASE_URL = "sqlite:///./dvd_rental.db"

# Параметр check_same_thread необходим только для SQLite
ENGINE = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
BASE = declarative_base()


# --- Модели таблиц (SQLAlchemy) ---


class Category(BASE):
    """Модель категорий (жанров) фильмов."""

    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    films = relationship("Film", back_populates="category")


class Film(BASE):
    """Модель информации о DVD-дисках."""

    __tablename__ = "films"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    release_year = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="films")
    rentals = relationship("Rental", back_populates="film")


class Customer(BASE):
    """Модель данных клиента."""

    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True)

    rentals = relationship("Rental", back_populates="customer")


class Staff(BASE):
    """Модель сотрудников проката."""

    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String)

    rentals = relationship("Rental", back_populates="staff")


class Rental(BASE):
    """Модель факта аренды диска."""

    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("films.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    staff_id = Column(Integer, ForeignKey("staff.id"))
    rental_date = Column(DateTime, default=datetime.now)
    return_date = Column(DateTime, nullable=True)

    film = relationship("Film", back_populates="rentals")
    customer = relationship("Customer", back_populates="rentals")
    staff = relationship("Staff", back_populates="rentals")


# Создание таблиц в файле БД
BASE.metadata.create_all(bind=ENGINE)


# --- Схемы данных (Pydantic) ---


class CategoryBase(BaseModel):
    """Базовая схема категории для валидации входных данных."""

    name: str


class CategorySchema(CategoryBase):
    """Схема категории для возврата данных через API."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class FilmBase(BaseModel):
    """Базовая схема фильма для валидации входных данных."""

    title: str
    description: Optional[str] = None
    release_year: int
    category_id: int


class FilmSchema(FilmBase):
    """Схема фильма для возврата данных через API."""

    id: int
    model_config = ConfigDict(from_attributes=True)


# --- Инициализация API ---

app = FastAPI(title="DVD Rental API (SQLite)")


# --- Зависимости ---


def get_db():
    """
    Генератор сессии базы данных.
    Обеспечивает закрытие соединения после завершения запроса.
    """
    database = SESSION_LOCAL()
    try:
        yield database
    finally:
        database.close()


# --- Эндпойнты (CRUD операции) ---


@app.post("/categories/", response_model=CategorySchema, tags=["Categories"])
def create_category(category: CategoryBase, db: Session = Depends(get_db)):
    """Добавляет новую категорию (жанр) в базу данных."""
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/films/", response_model=List[FilmSchema], tags=["Films"])
def read_films(db: Session = Depends(get_db)):
    """Возвращает список всех фильмов, зарегистрированных в системе."""
    return db.query(Film).all()


@app.post("/films/", response_model=FilmSchema, tags=["Films"])
def create_film(film: FilmBase, db: Session = Depends(get_db)):
    """
    Добавляет новый фильм.
    Перед добавлением убедитесь, что указанный category_id существует.
    """
    db_film = Film(**film.model_dump())
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film


@app.delete("/films/{film_id}", tags=["Films"])
def delete_film(film_id: int, db: Session = Depends(get_db)):
    """Удаляет фильм из базы данных по его идентификатору."""
    db_film = db.query(Film).filter(Film.id == film_id).first()
    if not db_film:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    db.delete(db_film)
    db.commit()
    return {"status": "success", "message": f"Фильм {film_id} удален"}


if __name__ == "__main__":
    import uvicorn

    # Запуск сервера на локальном хосте
    uvicorn.run(app, host="127.0.0.1", port=8000)
