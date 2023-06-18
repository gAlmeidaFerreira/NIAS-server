FROM python:3.9-slim

ARG QUEUE_PRODUCER_PORT

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && apt-get update\
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${QUEUE_PRODUCER_PORT}

CMD ["python", "./MessageProducer.py"]