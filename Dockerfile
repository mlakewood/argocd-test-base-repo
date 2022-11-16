FROM python:3.9-buster

RUN adduser webapp

USER webapp

RUN ls -la /home

WORKDIR /home/webapp

RUN python -m venv venv

RUN venv/bin/python -m pip install pip --upgrade
COPY requirements.txt /home/webapp/requirements.txt
RUN venv/bin/python -m pip install -r requirements.txt

COPY base_app.py /home/webapp/base_app.py

CMD venv/bin/python -m flask --app base_app run -h 0.0.0.0 -p 5000