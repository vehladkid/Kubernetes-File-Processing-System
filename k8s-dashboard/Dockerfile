# Dockerfile for Flask Dashboard
FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir flask

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

EXPOSE 8080

CMD ["flask", "run"]
