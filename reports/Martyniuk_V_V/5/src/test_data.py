"""Скрипт для тестирования API."""

import time
import requests

BASE_URL = "http://localhost:8000"


def test_api():
    """Тестирование всех эндпоинтов API."""
    print("Начинаем тестирование API...")
    print("=" * 50)

    print("1. Создаём группу...")
    response = requests.post(f"{BASE_URL}/groups", json={"name": "ИВТ-41"}, timeout=10)
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    group_id = response.json()["id"]

    print("\n2. Создаём преподавателя...")
    response = requests.post(
        f"{BASE_URL}/teachers", json={"name": "Смирнова Анна Петровна"}, timeout=10
    )
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    teacher_id = response.json()["id"]

    print("\n3. Создаём предмет...")
    response = requests.post(
        f"{BASE_URL}/subjects",
        json={"name": "Python", "teacher_id": teacher_id},
        timeout=10,
    )
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    subject_id = response.json()["id"]

    print("\n4. Создаём студента...")
    response = requests.post(
        f"{BASE_URL}/students",
        json={"name": "Сидоров Алексей", "group_id": group_id},
        timeout=10,
    )
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    student_id = response.json()["id"]

    print("\n5. Выставляем оценки...")
    response = requests.post(
        f"{BASE_URL}/grades",
        json={"value": 90, "student_id": student_id, "subject_id": subject_id},
        timeout=10,
    )
    print(f"   Оценка 90: {response.status_code}")

    response = requests.post(
        f"{BASE_URL}/grades",
        json={"value": 75, "student_id": student_id, "subject_id": subject_id},
        timeout=10,
    )
    print(f"   Оценка 75: {response.status_code}")

    print("\n6. Получаем оценки студента...")
    response = requests.get(f"{BASE_URL}/grades/{student_id}", timeout=10)
    print(f"   Статус: {response.status_code}")
    print(f"   Оценки: {response.json()}")

    print("\n7. Получаем средний балл...")
    response = requests.get(f"{BASE_URL}/average/{student_id}", timeout=10)
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")

    print("\n8. Получаем список всех студентов...")
    response = requests.get(f"{BASE_URL}/students", timeout=10)
    print(f"   Статус: {response.status_code}")
    print(f"   Студенты: {response.json()}")

    print("\n" + "=" * 50)
    print("Тестирование завершено!")
    print("\nДокументация API: http://localhost:8000/docs")


if __name__ == "__main__":
    print("Убедитесь, что сервер запущен (uvicorn main:app --reload)")
    print("Запустите этот скрипт в другом терминале")
    time.sleep(2)
    test_api()
