# Dockerfile
FROM python:3.12-slim

# устанавливаем poetry
RUN pip install poetry==1.8.2

# создаём рабочую директорию
WORKDIR /app

# копируем файлы с зависимостями
COPY pyproject.toml poetry.lock* ./

# устанавливаем зависимости (без установки самого проекта)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# копируем весь код
COPY . .

# указываем команду по умолчанию
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]