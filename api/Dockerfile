FROM python:3.11-slim

WORKDIR /api

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]