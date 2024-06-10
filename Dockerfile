FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install poetry && \
  poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-ansi --only main

CMD python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000