# task-service/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# ШАГ 2.1: ДОБАВЛЕНО ПО ЗАДАНИЮ ДЛЯ SSL-СЕРТИФИКАТОВ
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates openssl \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
 && pip install --upgrade pip \
 && pip install -r requirements.txt \
 && apt-get remove -y build-essential python3-dev \
 && apt-get autoremove -y && apt-get clean

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]