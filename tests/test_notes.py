import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Отдельная тестовая база — отдельный sqlite-файл, чтобы не трогать notes.db,
# которым пользуешься при обычном запуске приложения.
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    """Перед каждым тестом создаём чистые таблицы, после — удаляем."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_create_note():
    response = client.post("/notes/", json={"title": "Первая заметка", "content": "Текст заметки"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Первая заметка"
    assert "id" in data


def test_read_notes_empty():
    response = client.get("/notes/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_single_note():
    create_response = client.post("/notes/", json={"title": "Заметка", "content": "Содержимое"})
    note_id = create_response.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Заметка"


def test_read_note_not_found():
    response = client.get("/notes/999")
    assert response.status_code == 404


def test_update_note():
    create_response = client.post("/notes/", json={"title": "Старое", "content": "Старый текст"})
    note_id = create_response.json()["id"]

    response = client.put(f"/notes/{note_id}", json={"title": "Новое"})
    assert response.status_code == 200
    assert response.json()["title"] == "Новое"
    assert response.json()["content"] == "Старый текст"  # не менялось


def test_delete_note():
    create_response = client.post("/notes/", json={"title": "Удалить меня", "content": "..."})
    note_id = create_response.json()["id"]

    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 204

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 404
