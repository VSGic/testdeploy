FROM python:3.11-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt update &apt install curl -y

COPY ./app .

CMD ["python", "app.py"]
