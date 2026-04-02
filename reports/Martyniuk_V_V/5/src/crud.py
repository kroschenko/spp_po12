"""CRUD операции для работы с базой данных."""

from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Student, Group, Teacher, Subject, Grade
import schemas


def get_students(db: Session, skip: int = 0, limit: int = 100):
    """Получить список всех студентов с пагинацией."""
    return db.query(Student).offset(skip).limit(limit).all()


def get_student(db: Session, student_id: int):
    """Получить студента по ID."""
    return db.query(Student).filter(Student.id == student_id).first()


def create_student(db: Session, student: schemas.StudentCreate):
    """Создать нового студента."""
    db_student = Student(name=student.name, group_id=student.group_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student_data: schemas.StudentUpdate):
    """Обновить данные студента."""
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    if student_data.name is not None:
        db_student.name = student_data.name
    if student_data.group_id is not None:
        db_student.group_id = student_data.group_id
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    """Удалить студента."""
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    db.delete(db_student)
    db.commit()
    return db_student


def get_groups(db: Session):
    """Получить список всех групп."""
    return db.query(Group).all()


def get_group(db: Session, group_id: int):
    """Получить группу по ID."""
    return db.query(Group).filter(Group.id == group_id).first()


def create_group(db: Session, group: schemas.GroupCreate):
    """Создать новую группу."""
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_teachers(db: Session):
    """Получить список всех преподавателей."""
    return db.query(Teacher).all()


def get_teacher(db: Session, teacher_id: int):
    """Получить преподавателя по ID."""
    return db.query(Teacher).filter(Teacher.id == teacher_id).first()


def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    """Создать нового преподавателя."""
    db_teacher = Teacher(name=teacher.name)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def get_subjects(db: Session):
    """Получить список всех предметов."""
    return db.query(Subject).all()


def get_subject(db: Session, subject_id: int):
    """Получить предмет по ID."""
    return db.query(Subject).filter(Subject.id == subject_id).first()


def create_subject(db: Session, subject: schemas.SubjectCreate):
    """Создать новый предмет."""
    db_subject = Subject(name=subject.name, teacher_id=subject.teacher_id)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def get_grades_by_student(db: Session, student_id: int):
    """Получить все оценки студента."""
    return db.query(Grade).filter(Grade.student_id == student_id).all()


def create_grade(db: Session, grade: schemas.GradeCreate):
    """Создать новую оценку."""
    db_grade = Grade(
        value=grade.value, student_id=grade.student_id, subject_id=grade.subject_id
    )
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


def get_average_grade(db: Session, student_id: int):
    """Получить средний балл студента."""
    result = (
        db.query(func.avg(Grade.value)).filter(Grade.student_id == student_id).scalar()
    )
    return result if result else 0.0
