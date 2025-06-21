FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

VOLUME ["/app/data"]

EXPOSE 8000

ENV DATA_DIR=/app/data

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "app:app"]