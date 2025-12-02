FROM python:3.10-slim
WORKDIR /app
COPY app.py /app
RUN pip install flask
VOLUME ["/uploads"]
EXPOSE 8080
CMD ["python", "app.py"]
