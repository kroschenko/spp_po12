"""
Модуль для настройки подключения к базе данных PostgreSQL.
Создает движок SQLAlchemy и фабрику сессий.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Формат: postgresql://пользователь:пароль@хост/название_базы
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:41398754ki@localhost/travel_agency"

# Создаем "движок" для подключения к БД
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем фабрику сессий
# pylint: disable=invalid-name
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей
Base = declarative_base()


def get_db():
    """
    Генератор для получения сессии базы данных.
    Используется в FastAPI как зависимость для автоматического закрытия сессии.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
