FROM python:3.9-slim

RUN pip install fastapi uvicorn

EXPOSE 80

COPY . /app

CMD ["uvicorn", "app.setup:app", "--host", "0.0.0.0", "--port", "80"]
