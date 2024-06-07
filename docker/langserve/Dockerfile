FROM python:3.11-slim-bullseye

RUN groupadd --gid 1000 mygroup \
    && useradd --uid 1000 --gid mygroup myuser

# Install required packages
RUN apt update && apt install -y git

USER myuser

WORKDIR /app

RUN git clone   .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .