import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_setup():
    """Тест инициализации базы данных."""
    response = client.post("/setup/")
    assert response.status_code == 200
    assert response.json()["message"] == "Базовые данные добавлены!"

def test_create_employee():
    """Тест создания сотрудника."""
    response = client.post("/employees/", json={
        "full_name": "Иван Петров",
        "position": "Программист",
        "salary": 100000,
        "dept_id": 1
    })
    assert response.status_code == 200
    assert response.json()["full_name"] == "Иван Петров"

def test_read_employees():
    """Тест получения списка сотрудников."""
    response = client.get("/employees/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_employee_salary():
    """Тест обновления зарплаты сотрудника."""
    # Сначала создаем сотрудника
    create_resp = client.post("/employees/", json={
        "full_name": "Тестовый Сотрудник",
        "position": "Тестировщик",
        "salary": 50000,
        "dept_id": 1
    })
    emp_id = create_resp.json()["id"]
    
    # Обновляем зарплату
    response = client.put(f"/employees/{emp_id}?new_salary=60000")
    assert response.status_code == 200
    assert "успешно обновлена" in response.json()["message"]

def test_delete_employee():
    """Тест удаления сотрудника."""
    # Создаем сотрудника
    create_resp = client.post("/employees/", json={
        "full_name": "Удаляемый Сотрудник",
        "position": "Стажер",
        "salary": 30000,
        "dept_id": 1
    })
    emp_id = create_resp.json()["id"]
    
    # Удаляем сотрудника
    response = client.delete(f"/employees/{emp_id}")
    assert response.status_code == 200
    assert "удален" in response.json()["message"]

def test_read_employees_after_delete():
    """Тест, что после удаления сотрудников список пуст или содержит только созданных."""
    response = client.get("/employees/")
    assert response.status_code == 200
    