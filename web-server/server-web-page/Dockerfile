FROM python:3.9-slim

ARG WEB_PAGE_PORT

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip\
    && pip install -r requirements.txt\
    && mkdir ./output

COPY . .

EXPOSE ${WEB_PAGE_PORT}
CMD ["python", "main.py"]