import os

# По умолчанию используем локальный SQLite-файл — удобно для быстрого
# запуска без Docker и Postgres. Если переменная окружения DATABASE_URL
# задана (например, в docker-compose), используется она — там будет
# указан Postgres.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./notes.db")
