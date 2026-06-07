import pytest
import sys
import os
from fastapi.testclient import TestClient

# Добавляем родительскую папку (backend/) в путь, чтобы Python нашёл main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_health():
    """
    Тест 1: проверяем, что сервер отвечает на /api/health
    """
    # Отправляем GET-запрос на /api/health
    response = client.get("/api/health")

    # Проверяем, что код ответа — 200 (успех)
    assert response.status_code == 200

    # Проверяем, что в ответе есть поле status со значением "ok"
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "Chayan Tracker v1.0"


def test_create_and_get_note():
    """
    Тест 2: создаём заметку и получаем её обратно
    """
    # Данные для новой заметки
    new_note = {
        "title": "Тестовая заметка",
        "content": "Эту заметку создал робот во время теста"
    }

    # Отправляем POST-запрос для создания заметки
    response = client.post("/api/notes", json=new_note)

    # Проверяем, что код ответа — 200 (успех)
    assert response.status_code == 200

    # Проверяем, что в ответе есть id заметки
    data = response.json()
    assert "id" in data

    # Теперь получаем список всех заметок
    response = client.get("/api/notes")
    assert response.status_code == 200

    # Проверяем, что наша заметка есть в списке
    notes = response.json()
    titles = [note["title"] for note in notes]
    assert "Тестовая заметка" in titles
