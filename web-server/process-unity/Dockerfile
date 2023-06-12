FROM python:3.9-slim

ARG PROCESS_UNITY_PORT

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && apt-get update\
    && pip install --no-cache-dir -r requirements.txt\
    && mkdir output

COPY . .

EXPOSE ${PROCESS_UNITY_PORT}

CMD ["python", "./serv-tcp.py"]
