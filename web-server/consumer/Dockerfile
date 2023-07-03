FROM python:3.9-slim

ARG QUEUE_CONSUMER_PORT

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE ${QUEUE_CONSUMER_PORT}

CMD ["python", "MessageConsumer.py"]