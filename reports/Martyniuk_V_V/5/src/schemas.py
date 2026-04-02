"""Pydantic схемы для валидации данных."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class GroupBase(BaseModel):
    """Базовая схема группы."""

    name: str


class GroupCreate(GroupBase):
    """Схема для создания группы."""

    pass


class GroupResponse(GroupBase):
    """Схема ответа с данными группы."""

    id: int

    class Config:
        """Настройка схемы."""

        from_attributes = True


class StudentBase(BaseModel):
    """Базовая схема студента."""

    name: str
    group_id: int


class StudentCreate(StudentBase):
    """Схема для создания студента."""

    pass


class StudentUpdate(BaseModel):
    """Схема для обновления студента."""

    name: Optional[str] = None
    group_id: Optional[int] = None


class StudentResponse(StudentBase):
    """Схема ответа с данными студента."""

    id: int

    class Config:
        """Настройка схемы."""

        from_attributes = True


class TeacherBase(BaseModel):
    """Базовая схема преподавателя."""

    name: str


class TeacherCreate(TeacherBase):
    """Схема для создания преподавателя."""

    pass


class TeacherResponse(TeacherBase):
    """Схема ответа с данными преподавателя."""

    id: int

    class Config:
        """Настройка схемы."""

        from_attributes = True


class SubjectBase(BaseModel):
    """Базовая схема предмета."""

    name: str
    teacher_id: int


class SubjectCreate(SubjectBase):
    """Схема для создания предмета."""

    pass


class SubjectResponse(SubjectBase):
    """Схема ответа с данными предмета."""

    id: int

    class Config:
        """Настройка схемы."""

        from_attributes = True


class GradeBase(BaseModel):
    """Базовая схема оценки."""

    value: float
    student_id: int
    subject_id: int


class GradeCreate(GradeBase):
    """Схема для создания оценки."""

    pass


class GradeResponse(GradeBase):
    """Схема ответа с данными оценки."""

    id: int
    date: datetime

    class Config:
        """Настройка схемы."""

        from_attributes = True


class StudentWithDetails(StudentResponse):
    """Схема студента с деталями."""

    group: GroupResponse
    grades: List[GradeResponse] = []


class SubjectWithTeacher(SubjectResponse):
    """Схема предмета с преподавателем."""

    teacher: TeacherResponse
