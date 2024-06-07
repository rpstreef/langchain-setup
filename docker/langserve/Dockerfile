FROM python:3.11-slim-bullseye

# Install required packages
RUN apt update && apt install -y git

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

USER 1001

CMD ["uvicorn", "langserve:app", "--host", "0.0.0.0", "--port", "8080"]