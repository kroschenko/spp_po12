"""Главный модуль приложения FastAPI."""

# pylint: disable=too-few-public-methods

from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Education System API")


# --- СХЕМЫ PYDANTIC ---


class BaseSchema(BaseModel):
    """Базовая схема с включенным orm_mode."""

    class Config:
        """Настройки Pydantic."""

        from_attributes = True


class CourseSchema(BaseSchema):
    """Схема создания курса."""

    title: str
    teacher_id: int


class StudentSchema(BaseSchema):
    """Схема создания студента."""

    full_name: str
    faculty_id: int


class TeacherSchema(BaseSchema):
    """Схема создания преподавателя."""

    full_name: str
    email: str
    faculty_id: int


class FacultySchema(BaseSchema):
    """Схема создания факультета."""

    name: str
    institution_id: int


class InstitutionSchema(BaseSchema):
    """Схема создания учебного заведения."""

    name: str
    address: str


class InstitutionOut(InstitutionSchema):
    """Схема ответа для учебного заведения."""

    id: int


class FacultyOut(FacultySchema):
    """Схема ответа для факультета."""

    id: int


class TeacherOut(TeacherSchema):
    """Схема ответа для преподавателя."""

    id: int


class StudentOut(StudentSchema):
    """Схема ответа для студента."""

    id: int


class CourseOut(CourseSchema):
    """Схема ответа для курса."""

    id: int


# --- ЭНДПОИНТ ДЛЯ UML ДИАГРАММЫ ---


@app.get("/diagram", response_class=HTMLResponse, tags=["System"])
def get_uml_diagram():
    """Возвращает HTML-страницу с UML-диаграммой базы данных."""
    mermaid_code = """
    erDiagram
        INSTITUTION ||--o{ FACULTY : "имеет"
        FACULTY ||--o{ TEACHER : "нанимает"
        FACULTY ||--o{ STUDENT : "обучает"
        TEACHER ||--o{ COURSE : "преподает"

        INSTITUTION {
            int id PK
            string name
            string address
        }
        FACULTY {
            int id PK
            string name
            int institution_id FK "Внешний ключ"
        }
        TEACHER {
            int id PK
            string full_name
            string email
            int faculty_id FK "Внешний ключ"
        }
        STUDENT {
            int id PK
            string full_name
            int faculty_id FK "Внешний ключ"
        }
        COURSE {
            int id PK
            string title
            int teacher_id FK "Внешний ключ"
        }
    """
    return f"""
    <html>
        <head>
            <title>Схема БД</title>
            <style>
                body {{ display: flex; justify-content: center; padding: 20px; }}
            </style>
        </head>
        <body>
            <div class="mermaid">
                {mermaid_code}
            </div>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
            </script>
        </body>
    </html>
    """


# --- CRUD ОПЕРАЦИИ ДЛЯ ВСЕХ ТАБЛИЦ ---


@app.post("/institutions/", response_model=InstitutionOut, tags=["Institutions"])
def create_institution(item: InstitutionSchema, db: Session = Depends(get_db)):
    """Создает новое учебное заведение."""
    db_item = models.Institution(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/institutions/", response_model=List[InstitutionOut], tags=["Institutions"])
def list_institutions(db: Session = Depends(get_db)):
    """Возвращает список всех учебных заведений."""
    return db.query(models.Institution).all()


@app.put(
    "/institutions/{item_id}", response_model=InstitutionOut, tags=["Institutions"]
)
def update_institution(
    item_id: int, item: InstitutionSchema, db: Session = Depends(get_db)
):
    """Обновляет данные учебного заведения по ID."""
    db_item = (
        db.query(models.Institution).filter(models.Institution.id == item_id).first()
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.post("/faculties/", response_model=FacultyOut, tags=["Faculties"])
def create_faculty(item: FacultySchema, db: Session = Depends(get_db)):
    """Создает новый факультет."""
    db_item = models.Faculty(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/faculties/", response_model=List[FacultyOut], tags=["Faculties"])
def list_faculties(db: Session = Depends(get_db)):
    """Возвращает список всех факультетов."""
    return db.query(models.Faculty).all()


@app.put("/faculties/{item_id}", response_model=FacultyOut, tags=["Faculties"])
def update_faculty(item_id: int, item: FacultySchema, db: Session = Depends(get_db)):
    """Обновляет данные факультета по ID."""
    db_item = db.query(models.Faculty).filter(models.Faculty.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.post("/teachers/", response_model=TeacherOut, tags=["Teachers"])
def create_teacher(item: TeacherSchema, db: Session = Depends(get_db)):
    """Создает нового преподавателя."""
    db_item = models.Teacher(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/teachers/", response_model=List[TeacherOut], tags=["Teachers"])
def list_teachers(db: Session = Depends(get_db)):
    """Возвращает список всех преподавателей."""
    return db.query(models.Teacher).all()


@app.put("/teachers/{item_id}", response_model=TeacherOut, tags=["Teachers"])
def update_teacher(item_id: int, item: TeacherSchema, db: Session = Depends(get_db)):
    """Обновляет данные преподавателя по ID."""
    db_item = db.query(models.Teacher).filter(models.Teacher.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.post("/students/", response_model=StudentOut, tags=["Students"])
def create_student(item: StudentSchema, db: Session = Depends(get_db)):
    """Создает нового студента."""
    db_item = models.Student(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/students/", response_model=List[StudentOut], tags=["Students"])
def list_students(db: Session = Depends(get_db)):
    """Возвращает список всех студентов."""
    return db.query(models.Student).all()


@app.put("/students/{item_id}", response_model=StudentOut, tags=["Students"])
def update_student(item_id: int, item: StudentSchema, db: Session = Depends(get_db)):
    """Обновляет данные студента по ID."""
    db_item = db.query(models.Student).filter(models.Student.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.post("/courses/", response_model=CourseOut, tags=["Courses"])
def create_course(item: CourseSchema, db: Session = Depends(get_db)):
    """Создает новый курс."""
    db_item = models.Course(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/courses/", response_model=List[CourseOut], tags=["Courses"])
def list_courses(db: Session = Depends(get_db)):
    """Возвращает список всех курсов."""
    return db.query(models.Course).all()


@app.put("/courses/{item_id}", response_model=CourseOut, tags=["Courses"])
def update_course(item_id: int, item: CourseSchema, db: Session = Depends(get_db)):
    """Обновляет данные курса по ID."""
    db_item = db.query(models.Course).filter(models.Course.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/clear/{table_name}/{item_id}", tags=["System"])
def delete_item(table_name: str, item_id: int, db: Session = Depends(get_db)):
    """Удаляет запись из указанной таблицы по ID."""
    models_map = {
        "institution": models.Institution,
        "faculty": models.Faculty,
        "teacher": models.Teacher,
        "student": models.Student,
        "course": models.Course,
    }
    model = models_map.get(table_name.lower())
    if not model:
        raise HTTPException(status_code=400, detail="Table not found")

    db_item = db.query(model).filter(model.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"status": "deleted", "table": table_name, "id": item_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
