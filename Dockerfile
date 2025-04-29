# syntax=docker/dockerfile:1
FROM python:3.12-rc-slim-buster
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app.py app.py
COPY Top_10000_Movies_IMDb.csv Top_10000_Movies_IMDb.csv

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
