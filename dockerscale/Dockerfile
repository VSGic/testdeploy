FROM python:3.11

WORKDIR /app

COPY ./dockerscale .

RUN pip install --no-cache-dir flask docker requests==2.31.0 

RUN apt update & apt install -y curl

CMD ["python3", "dockerscale.py"]

