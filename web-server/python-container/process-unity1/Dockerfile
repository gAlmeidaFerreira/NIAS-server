FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt\
    && mkdir output

COPY . .

EXPOSE 5000

CMD ["python", "./serv-tcp.py"]
