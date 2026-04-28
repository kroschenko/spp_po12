from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

# Создание таблиц в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API (Variant 6)")


@app.post("/books/", response_model=schemas.BookResponse, tags=["Books"])
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Добавление новой книги"""
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/", response_model=list[schemas.BookResponse], tags=["Books"])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получение списка книг"""
    return db.query(models.Book).offset(skip).limit(limit).all()


@app.get("/books/{book_id}", response_model=schemas.BookResponse, tags=["Books"])
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Получение одной книги по ID"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.BookResponse, tags=["Books"])
def update_book(book_id: int, book_update: schemas.BookCreate, db: Session = Depends(get_db)):
    """Обновление данных о книге"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_update.model_dump().items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удаление книги"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": f"Book with id {book_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
