FROM python:3.12-slim

WORKDIR /app

COPY backend/pyproject.toml ./backend/pyproject.toml

RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    sqlalchemy \
    pydantic \
    python-dotenv

COPY backend ./backend

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]