FROM python:3.9-slim

ARG WEB_PAGE_PORT

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE ${WEB_PAGE_PORT}
CMD ["python", "main.py"]