# Notes API

Простое REST API для заметок (CRUD) на FastAPI + SQLAlchemy + PostgreSQL.
Pet-проект для портфолио.

## Что умеет

- `POST /notes/` — создать заметку
- `GET /notes/` — получить список заметок
- `GET /notes/{id}` — получить одну заметку
- `PUT /notes/{id}` — обновить заметку (можно частично: только title или только content)
- `DELETE /notes/{id}` — удалить заметку

После запуска вся документация и ручное тестирование эндпоинтов доступны
на `http://localhost:8000/docs` (это Swagger UI, он генерируется автоматически).

## Структура проекта

```
app/
├── main.py            # точка входа, создаёт приложение и подключает роутер
├── config.py           # читает настройки (DATABASE_URL) из окружения
├── database.py         # engine, сессии, подключение к БД
├── models.py            # SQLAlchemy-модель таблицы Note
├── schemas.py            # Pydantic-схемы: что приходит и что отдаёт API
├── crud.py                # вся работа с базой (отдельно от роутера)
└── routers/
    └── notes.py            # сами эндпоинты /notes

tests/
└── test_notes.py            # тесты на эндпоинты (pytest)
```

Логика специально разложена по слоям: роутер только принимает запрос и
вызывает `crud`, `crud` работает с базой через SQLAlchemy, `schemas`
отвечает за то, что лежит в теле запроса/ответа. Это стандартный паттерн —
на собеседовании такое разделение будет плюсом.

## Запуск — вариант 1: быстро, локально, без Docker

Не нужен Postgres — по умолчанию используется SQLite-файл (`notes.db`),
который создастся автоматически.

```bash
python -m venv venv
source venv/bin/activate        # на Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Открой в браузере: http://localhost:8000/docs

## Запуск — вариант 2: через Docker (с настоящим Postgres)

 используется
`docker-compose`, поднимается отдельный контейнер с Postgres.

```bash
docker compose up --build
```

Приложение будет на http://localhost:8000/docs, база данных — в отдельном
контейнере Postgres (данные сохраняются между перезапусками в volume `pgdata`).

## Тесты

```bash
pytest
```

Тесты используют отдельную тестовую SQLite-базу (`test.db`), не трогая
основную — перед каждым тестом таблицы создаются заново, после — удаляются.

## Пример запроса (curl)

```bash
curl -X POST http://localhost:8000/notes/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Моя первая заметка", "content": "Привет, FastAPI!"}'
```

## Возможные доработки

- Авторизация пользователей (JWT), чтобы у каждого были свои заметки
- Пагинация и поиск по заголовку
- Миграции через Alembic вместо `Base.metadata.create_all`
- Деплой на реальный сервер (например, на Render или VPS)
