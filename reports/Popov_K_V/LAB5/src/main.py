"""
Главный модуль приложения FastAPI для управления турагентством.
Реализует CRUD операции для работы с данными о турах.
"""

from datetime import date
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import engine, get_db
import models

# Создаем таблицы в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Agency API")


# pylint: disable=too-few-public-methods
class TourBase(BaseModel):
    """Базовая схема Pydantic для данных тура."""
    name: str
    country: str
    price: float
    start_date: date
    end_date: date


class TourCreate(TourBase):
    """Схема для создания или обновления тура."""


class TourResponse(TourBase):
    """Схема для ответа API, включающая автоматически созданный ID."""
    id: int

    class Config:
        """Настройки для работы Pydantic с моделями SQLAlchemy."""
        from_attributes = True


@app.post("/tours/", response_model=TourResponse, summary="Добавить новый тур")
def create_tour(tour: TourCreate, db: Session = Depends(get_db)):
    """
    Создает новую запись о туре в базе данных.
    """
    db_tour = models.Tour(
        name=tour.name,
        country=tour.country,
        price=tour.price,
        start_date=tour.start_date,
        end_date=tour.end_date
    )
    db.add(db_tour)
    db.commit()
    db.refresh(db_tour)
    return db_tour


@app.get("/tours/", response_model=List[TourResponse], summary="Список всех туров")
def read_tours(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Возвращает список туров из базы данных с поддержкой пагинации.
    """
    return db.query(models.Tour).offset(skip).limit(limit).all()


@app.get("/tours/{tour_id}", response_model=TourResponse, summary="Тур по ID")
def read_tour(tour_id: int, db: Session = Depends(get_db)):
    """
    Ищет в базе данных один конкретный тур по его идентификатору.
    """
    tour = db.query(models.Tour).filter(models.Tour.id == tour_id).first()
    if tour is None:
        raise HTTPException(status_code=404, detail="Тур не найден")
    return tour


@app.put("/tours/{tour_id}", response_model=TourResponse, summary="Обновить тур")
def update_tour(tour_id: int, tour_update: TourCreate, db: Session = Depends(get_db)):
    """
    Обновляет данные существующего тура (Модификация).
    """
    db_tour = db.query(models.Tour).filter(models.Tour.id == tour_id).first()
    if db_tour is None:
        raise HTTPException(status_code=404, detail="Тур не найден")

    db_tour.name = tour_update.name
    db_tour.country = tour_update.country
    db_tour.price = tour_update.price
    db_tour.start_date = tour_update.start_date
    db_tour.end_date = tour_update.end_date

    db.commit()
    db.refresh(db_tour)
    return db_tour


@app.delete("/tours/{tour_id}", summary="Удалить тур")
def delete_tour(tour_id: int, db: Session = Depends(get_db)):
    """
    Удаляет запись о туре из базы данных по указанному ID.
    """
    db_tour = db.query(models.Tour).filter(models.Tour.id == tour_id).first()
    if db_tour is None:
        raise HTTPException(status_code=404, detail="Тур не найден")
    db.delete(db_tour)
    db.commit()
    return {"message": f"Тур с ID {tour_id} успешно удален"}
