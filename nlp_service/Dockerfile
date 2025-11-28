FROM python:3.11-slim

WORKDIR /app

COPY ./nlp_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./nlp_service .
COPY ./broker /app/broker

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]