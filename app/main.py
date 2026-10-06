from fastapi import FastAPI

from app.database import Base, engine
from app.routers import notes

# Создаёт таблицы в БД при старте, если их ещё нет.
# Для pet-проекта этого достаточно; в реальном продакшене
# для этого используют миграции (Alembic).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API", version="1.0.0")

app.include_router(notes.router)


@app.get("/")
def root():
    return {"message": "Notes API is running. See /docs for the API documentation."}
