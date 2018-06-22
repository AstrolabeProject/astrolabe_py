FROM python:3.6.5

RUN mkdir /app
RUN mkdir /app/Hunter

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD flasktest.py .
ADD hunter.wtml .
Add Hunter Hunter

EXPOSE 5000

ENV FLASK_APP=flasktest.py

CMD ["flask", "run", "--host", "0.0.0.0"]
