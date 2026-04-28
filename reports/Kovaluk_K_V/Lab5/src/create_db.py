from datetime import date
from database import engine, Base, SessionLocal
from crud import create_client, create_manufacturer, create_product, create_computer

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    create_client(db, "Иван", "Петров", "M", "ivan_p", "+7(123)456-78-90", "ivan@mail.ru")
    create_client(db, "Мария", "Сидорова", "F", "masha_s", "+7(098)765-43-21", "maria@mail.ru")
    create_client(db, "Алексей", "Иванов", "M", None, "+7(555)123-45-67", "alex@mail.ru")
    print("Клиенты добавлены")

    man1 = create_manufacturer(db, "Intel Corporation", date(1968, 7, 18))
    man2 = create_manufacturer(db, "AMD", date(1969, 5, 1))
    man3 = create_manufacturer(db, "NVIDIA", date(1993, 4, 5))
    man4 = create_manufacturer(db, "ASUS", date(1989, 4, 2))
    man5 = create_manufacturer(db, "Kingston", date(1987, 10, 17))
    print("Производители добавлены")

    p1 = create_product(db, "Процессор Intel Core i9-13900K", 58990.00, man1.man_id)
    p2 = create_product(db, "Процессор AMD Ryzen 9 7950X", 54990.00, man2.man_id)
    p3 = create_product(db, "Видеокарта NVIDIA RTX 4090", 189990.00, man3.man_id)
    p4 = create_product(db, "Материнская плата ASUS ROG Maximus Z790", 45990.00, man4.man_id)
    p5 = create_product(db, "Оперативная память Kingston FURY 32GB", 12990.00, man5.man_id)
    p6 = create_product(db, "Видеокарта NVIDIA RTX 4080", 129990.00, man3.man_id)
    create_product(db, "Процессор Intel Core i7-13700K", 38990.00, man1.man_id)
    print("Продукты добавлены")

    create_computer(
        db, "SN001", "Gaming PC Ultra", "Intel Core i9-13900K",
        32, 1000, p1.pr_id, "available"
    )
    create_computer(
        db, "SN002", "Workstation Pro", "AMD Ryzen 9 7950X",
        64, 2000, p2.pr_id, "available"
    )
    create_computer(
        db, "SN003", "Gaming PC RTX", "Intel Core i7-13700K",
        32, 1000, p6.pr_id, "rented"
    )
    create_computer(
        db, "SN004", "Design Station", "AMD Ryzen 9 7950X",
        128, 4000, p3.pr_id, "maintenance"
    )
    print("Компьютеры добавлены")

    print("База данных успешно создана и заполнена тестовыми данными!")
    print("Добавлено клиентов: 3")
    print("Добавлено производителей: 5")
    print("Добавлено продуктов: 7")
    print("Добавлено компьютеров: 4")

except Exception as e:
    print(f"Ошибка: {e}")
    db.rollback()
finally:
    db.close()
