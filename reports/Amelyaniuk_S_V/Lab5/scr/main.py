from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database as db

app = FastAPI(title="Система Сборки ПК (Вариант 5)")


# Dependency для получения сессии БД
def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


# --- Операции для Компонентов (Components) ---


@app.post("/components/")
def create_component(
    name: str, price: float, cat_id: int, man_id: int, s: Session = Depends(get_db)
):
    new_item = db.Component(
        name=name, price=price, category_id=cat_id, manufacturer_id=man_id
    )
    s.add(new_item)
    s.commit()
    s.refresh(new_item)
    return new_item


@app.get("/components/")
def read_components(s: Session = Depends(get_db)):
    return s.query(db.Component).all()


@app.put("/components/{item_id}")
def update_component(item_id: int, new_price: float, s: Session = Depends(get_db)):
    item = s.query(db.Component).filter(db.Component.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Component not found")
    item.price = new_price
    s.commit()
    return {"message": "Price updated", "item": item}


@app.delete("/components/{item_id}")
def delete_component(item_id: int, s: Session = Depends(get_db)):
    item = s.query(db.Component).filter(db.Component.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    s.delete(item)
    s.commit()
    return {"status": "Deleted"}


# --- Операции для Категорий ---


@app.post("/categories/")
def add_category(name: str, s: Session = Depends(get_db)):
    cat = db.Category(name=name)
    s.add(cat)
    s.commit()
    return cat


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
