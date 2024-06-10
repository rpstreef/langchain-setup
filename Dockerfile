FROM python:3.11-slim

# Install poetry so we can install our package requirements
RUN pip3 install pipx && \
  pipx install poetry

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . /app

CMD exec uvicorn app.main:app --host 0.0.0.0 --port 8000  