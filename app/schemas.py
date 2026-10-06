from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    """Что присылает клиент при создании заметки."""
    title: str
    content: str


class NoteUpdate(BaseModel):
    """Что присылает клиент при обновлении — оба поля необязательны,
    чтобы можно было поменять только title или только content."""
    title: Optional[str] = None
    content: Optional[str] = None


class NoteOut(BaseModel):
    """Что API возвращает клиенту."""
    id: int
    title: str
    content: str
    created_at: datetime

    # Позволяет Pydantic читать данные прямо из объекта SQLAlchemy,
    # а не только из словаря (в Pydantic v1 это называлось orm_mode).
    model_config = ConfigDict(from_attributes=True)
