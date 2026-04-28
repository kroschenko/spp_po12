import pytest
from fastapi.testclient import TestClient
import os

# Проверяем, что файл базы данных существует
def test_db_exists():
    assert os.path.exists("accounting.db"), "accounting.db not found"

# Импортируем приложение
from main import app
client = TestClient(app)

def test_setup_endpoint():
    """Тест эндпоинта /setup/"""
    response = client.post("/setup/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_employees_endpoint():
    """Тест GET /employees/"""
    response = client.get("/employees/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_employee():
    """Тест POST /employees/"""
    response = client.post("/employees/", json={
        "full_name": "Test User",
        "position": "Developer",
        "salary": 100000,
        "dept_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Test User"
    assert "id" in data

def test_update_employee():
    """Тест PUT /employees/{emp_id}"""
    # Сначала создаем сотрудника
    create_resp = client.post("/employees/", json={
        "full_name": "Update Test",
        "position": "Tester",
        "salary": 50000,
        "dept_id": 1
    })
    emp_id = create_resp.json()["id"]
    
    # Обновляем зарплату
    response = client.put(f"/employees/{emp_id}?new_salary=75000")
    assert response.status_code == 200
    assert "успешно обновлена" in response.json()["message"]

def test_delete_employee():
    """Тест DELETE /employees/{emp_id}"""
    # Создаем сотрудника
    create_resp = client.post("/employees/", json={
        "full_name": "Delete Test",
        "position": "Intern",
        "salary": 30000,
        "dept_id": 1
    })
    emp_id = create_resp.json()["id"]
    
    # Удаляем
    response = client.delete(f"/employees/{emp_id}")
    assert response.status_code == 200
    assert "удален" in response.json()["message"]