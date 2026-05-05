"""Основной файл FastAPI для управления данными деканата."""
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import models

DATABASE_URL = "sqlite:///./deanery.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Deanery API")


def get_db():
    """Зависимость для получения сессии базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/groups/")
def read_groups(db: Session = Depends(get_db)):
    """Возвращает список всех групп."""
    return db.query(models.Group).all()
