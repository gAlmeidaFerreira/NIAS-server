FROM python:3.9-slim

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE ${WEB-PAGE_PORT}
CMD ["python", "main.py"]