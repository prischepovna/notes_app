from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import DATABASE_URL

# connect_args нужен только для SQLite (разрешает работу из разных потоков,
# что требуется для FastAPI + TestClient). Для Postgres он не нужен и не мешает.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency для FastAPI: открывает сессию на один запрос и закрывает её после."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
