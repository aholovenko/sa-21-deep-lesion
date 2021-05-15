FROM python:3.9-slim

COPY . /app

RUN pip install -r /app/requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.setup:app", "--host", "0.0.0.0", "--port", "80"]
