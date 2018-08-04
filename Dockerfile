FROM python:3.6-alpine

MAINTAINER Tom Hicks <hickst@email.arizona.edu>

RUN mkdir /app
WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ENV FLASK_APP=flasktest.py

CMD ["flask", "run", "--host", "0.0.0.0"]
