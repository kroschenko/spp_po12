"""FastAPI приложение для учёта успеваемости."""

from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base
import crud
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API учёта успеваемости",
    description="Лабораторная работа №5 - Учёт успеваемости студентов",
    version="1.0.0",
)


@app.get("/groups", response_model=List[schemas.GroupResponse], tags=["Groups"])
def get_groups(db: Session = Depends(get_db)):
    """Получить список всех групп."""
    return crud.get_groups(db)


@app.post(
    "/groups",
    response_model=schemas.GroupResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Groups"],
)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    """Создать новую группу."""
    return crud.create_group(db, group)


@app.get("/students", response_model=List[schemas.StudentResponse], tags=["Students"])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список студентов с пагинацией."""
    return crud.get_students(db, skip=skip, limit=limit)


@app.get(
    "/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"]
)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Получить студента по ID."""
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return student


@app.post(
    "/students",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Добавить нового студента."""
    group = crud.get_group(db, student.group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return crud.create_student(db, student)


@app.put(
    "/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"]
)
def update_student(
    student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)
):
    """Обновить данные студента."""
    updated = crud.update_student(db, student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return updated


@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Удалить студента."""
    deleted = crud.delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return {"message": f"Студент с ID {student_id} удалён", "deleted_id": student_id}


@app.get("/teachers", response_model=List[schemas.TeacherResponse], tags=["Teachers"])
def get_teachers(db: Session = Depends(get_db)):
    """Получить список всех преподавателей."""
    return crud.get_teachers(db)


@app.post(
    "/teachers",
    response_model=schemas.TeacherResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Teachers"],
)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    """Добавить нового преподавателя."""
    return crud.create_teacher(db, teacher)


@app.get("/subjects", response_model=List[schemas.SubjectResponse], tags=["Subjects"])
def get_subjects(db: Session = Depends(get_db)):
    """Получить список всех предметов."""
    return crud.get_subjects(db)


@app.post(
    "/subjects",
    response_model=schemas.SubjectResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Subjects"],
)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    """Добавить новый предмет."""
    teacher = crud.get_teacher(db, subject.teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    return crud.create_subject(db, subject)


@app.get(
    "/grades/{student_id}", response_model=List[schemas.GradeResponse], tags=["Grades"]
)
def get_student_grades(student_id: int, db: Session = Depends(get_db)):
    """Получить все оценки студента."""
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return crud.get_grades_by_student(db, student_id)


@app.post(
    "/grades",
    response_model=schemas.GradeResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Grades"],
)
def add_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    """Выставить оценку студенту."""
    student = crud.get_student(db, grade.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")

    subject = crud.get_subject(db, grade.subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Предмет не найден")

    if grade.value < 0 or grade.value > 100:
        raise HTTPException(status_code=400, detail="Оценка должна быть от 0 до 100")

    return crud.create_grade(db, grade)


@app.get("/average/{student_id}", tags=["Grades"])
def get_average_grade(student_id: int, db: Session = Depends(get_db)):
    """Получить средний балл студента."""
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")

    avg = crud.get_average_grade(db, student_id)
    return {
        "student_id": student_id,
        "student_name": student.name,
        "average_grade": round(avg, 2),
    }


@app.get("/", tags=["Root"])
def root():
    """Корневой эндпоинт с информацией об API."""
    return {
        "message": "API учёта успеваемости",
        "endpoints": {
            "groups": "/groups",
            "students": "/students",
            "teachers": "/teachers",
            "subjects": "/subjects",
            "grades": "/grades/{student_id}",
            "average": "/average/{student_id}",
        },
        "docs": "/docs",
    }
