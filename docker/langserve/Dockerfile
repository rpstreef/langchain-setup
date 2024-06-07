FROM python:3.11-slim-bullseye

RUN groupadd --gid 1000 mygroup \
    && useradd --uid 1000 --gid mygroup myuser

# Install required packages
RUN apt update && apt install -y git

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

USER myuser

CMD ["uvicorn", "langserve:app", "--host", "0.0.0.0", "--port", "8080"]