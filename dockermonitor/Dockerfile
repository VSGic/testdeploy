FROM python:3.11-slim

WORKDIR /app

COPY ./dockermonitor .

RUN pip install --no-cache-dir prometheus_api_client requests==2.31.0

CMD ["python3", "dockermonitor.py"]

