FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask docker requests==2.31.0
EXPOSE 5000
CMD ["python3", "dockerscale.py"]

