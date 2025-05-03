# syntax=docker/dockerfile:1
FROM python:3.12-rc-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
EXPOSE 5006

CMD ["flask", "run", "--host=0.0.0.0", "--port=5006"]
