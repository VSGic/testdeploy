FROM python:3.11-slim

WORKDIR /app

COPY ./dockerscale .

RUN pip install --no-cache-dir flask docker requests==2.31.0 curl

CMD ["python3", "dockerscale.py"]

