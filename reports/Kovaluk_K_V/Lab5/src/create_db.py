from database import engine, Base, SessionLocal
from crud import create_client, create_manufacturer, create_product, create_computer
from datetime import date

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

client1 = create_client(db, "Иван", "Петров", "M", "ivan_p", "+7(123)456-78-90", "ivan@mail.ru")
client2 = create_client(db, "Мария", "Сидорова", "F", "masha_s", "+7(098)765-43-21", "maria@mail.ru")
client3 = create_client(db, "Алексей", "Иванов", "M", None, "+7(555)123-45-67", "alex@mail.ru")

man1 = create_manufacturer(db, "Intel Corporation", date(1968, 7, 18))
man2 = create_manufacturer(db, "AMD", date(1969, 5, 1))
man3 = create_manufacturer(db, "NVIDIA", date(1993, 4, 5))
man4 = create_manufacturer(db, "ASUS", date(1989, 4, 2))
man5 = create_manufacturer(db, "Kingston", date(1987, 10, 17))

product1 = create_product(db, "Процессор Intel Core i9-13900K", 58990.00, man1.man_id)
product2 = create_product(db, "Процессор AMD Ryzen 9 7950X", 54990.00, man2.man_id)
product3 = create_product(db, "Видеокарта NVIDIA RTX 4090", 189990.00, man3.man_id)
product4 = create_product(db, "Материнская плата ASUS ROG Maximus Z790", 45990.00, man4.man_id)
product5 = create_product(db, "Оперативная память Kingston FURY 32GB", 12990.00, man5.man_id)
product6 = create_product(db, "Видеокарта NVIDIA RTX 4080", 129990.00, man3.man_id)
product7 = create_product(db, "Процессор Intel Core i7-13700K", 38990.00, man1.man_id)

computer1 = create_computer(db, "SN001", "Gaming PC Ultra", "Intel Core i9-13900K", 32, 1000, product1.pr_id, "available")
computer2 = create_computer(db, "SN002", "Workstation Pro", "AMD Ryzen 9 7950X", 64, 2000, product2.pr_id, "available")
computer3 = create_computer(db, "SN003", "Gaming PC RTX", "Intel Core i7-13700K", 32, 1000, product6.pr_id, "rented")
computer4 = create_computer(db, "SN004", "Design Station", "AMD Ryzen 9 7950X", 128, 4000, product3.pr_id, "maintenance")

print("База данных успешно создана и заполнена тестовыми данными!")
print(f"Добавлено клиентов: 3")
print(f"Добавлено производителей: 5")
print(f"Добавлено продуктов: 7")
print(f"Добавлено компьютеров: 4")

db.close()
