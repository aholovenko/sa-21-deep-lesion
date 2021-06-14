FROM python:3.9-slim

COPY . ./

RUN pip install -r ./requirements.txt

EXPOSE 80

CMD ["uvicorn", "setup:app", "--host", "0.0.0.0", "--port", "80"]
