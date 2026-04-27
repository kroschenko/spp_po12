"""Скрипт для тестирования API."""

import time
import requests

BASE_URL = "http://localhost:8000"


def create_group():
    """Создание группы."""
    print("1. Создаём группу...")
    response = requests.post(f"{BASE_URL}/groups", json={"name": "ИВТ-41"}, timeout=10)
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    return response.json()["id"]


def create_teacher():
    """Создание преподавателя."""
    print("\n2. Создаём преподавателя...")
    response = requests.post(
        f"{BASE_URL}/teachers",
        json={"name": "Смирнова Анна Петровна"},
        timeout=10
    )
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    return response.json()["id"]


def create_subject(teacher_id):
    """Создание предмета."""
    print("\n3. Создаём предмет...")
    response = requests.post(
        f"{BASE_URL}/subjects",
        json={"name": "Python", "teacher_id": teacher_id},
        timeout=10
    )
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    return response.json()["id"]


def create_student(group_id):
    """Создание студента."""
    print("\n4. Создаём студента...")
    response = requests.post(
        f"{BASE_URL}/students",
        json={"name": "Сидоров Алексей", "group_id": group_id},
        timeout=10
    )
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    return response.json()["id"]


def add_grades(student_id, subject_id):
    """Добавление оценок."""
    print("\n5. Выставляем оценки...")
    response = requests.post(
        f"{BASE_URL}/grades",
        json={"value": 90, "student_id": student_id, "subject_id": subject_id},
        timeout=10
    )
    print(f"   Оценка 90: {response.status_code}")

    response = requests.post(
        f"{BASE_URL}/grades",
        json={"value": 75, "student_id": student_id, "subject_id": subject_id},
        timeout=10
    )
    print(f"   Оценка 75: {response.status_code}")


def get_student_grades(student_id):
    """Получение оценок студента."""
    print("\n6. Получаем оценки студента...")
    response = requests.get(f"{BASE_URL}/grades/{student_id}", timeout=10)
    print(f"   Статус: {response.status_code}")
    print(f"   Оценки: {response.json()}")


def get_average(student_id):
    """Получение среднего балла."""
    print("\n7. Получаем средний балл...")
    response = requests.get(f"{BASE_URL}/average/{student_id}", timeout=10)
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")


def get_all_students():
    """Получение всех студентов."""
    print("\n8. Получаем список всех студентов...")
    response = requests.get(f"{BASE_URL}/students", timeout=10)
    print(f"   Статус: {response.status_code}")
    print(f"   Студенты: {response.json()}")


def test_api():
    """Тестирование всех эндпоинтов API."""
    print("Начинаем тестирование API...")
    print("=" * 50)

    group_id = create_group()
    teacher_id = create_teacher()
    subject_id = create_subject(teacher_id)
    student_id = create_student(group_id)
    add_grades(student_id, subject_id)
    get_student_grades(student_id)
    get_average(student_id)
    get_all_students()

    print("\n" + "=" * 50)
    print("Тестирование завершено!")
    print("\nДокументация API: http://localhost:8000/docs")


if __name__ == "__main__":
    print("Убедитесь, что сервер запущен (uvicorn main:app --reload)")
    print("Запустите этот скрипт в другом терминале")
    time.sleep(2)
    test_api()
