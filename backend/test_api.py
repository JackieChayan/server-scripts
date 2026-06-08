import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    """
    Тест 1: проверяем, что сервер отвечает на /api/health
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "Chayan Tracker v1.0"


# Тест с базой данных пока пропускаем — для него нужен PostgreSQL в CI
# def test_create_and_get_note():
#     ...
