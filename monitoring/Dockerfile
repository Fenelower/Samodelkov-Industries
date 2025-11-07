FROM python:3.10-slim

WORKDIR /app

COPY custom_exporter.py .

RUN pip install prometheus_client psycopg2-binary

CMD ["python", "custom_exporter.py"]
