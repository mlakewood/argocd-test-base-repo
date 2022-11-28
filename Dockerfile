FROM python:3.9-buster as integration-tests

RUN adduser webapp

USER webapp

RUN ls -la /home

WORKDIR /home/webapp

RUN python -m venv venv

RUN venv/bin/python -m pip install pip --upgrade
COPY test_requirements.txt /home/webapp/requirements.txt
RUN venv/bin/python -m pip install -r requirements.txt

COPY test_app.py /home/webapp/test_app.py

CMD venv/bin/python -m pytest .

FROM python:3.9-buster as front-app

RUN adduser webapp

USER webapp

RUN ls -la /home

WORKDIR /home/webapp

RUN python -m venv venv

RUN venv/bin/python -m pip install pip --upgrade
COPY requirements.txt /home/webapp/requirements.txt
RUN venv/bin/python -m pip install -r requirements.txt

COPY front_app.py /home/webapp/front_app.py

CMD venv/bin/python -m flask --app front_app run -h 0.0.0.0 -p 5000


FROM python:3.9-buster as back-app

RUN adduser webapp

USER webapp

RUN ls -la /home

WORKDIR /home/webapp

RUN python -m venv venv

RUN venv/bin/python -m pip install pip --upgrade
COPY requirements.txt /home/webapp/requirements.txt
RUN venv/bin/python -m pip install -r requirements.txt

COPY back_app.py /home/webapp/back_app.py

CMD venv/bin/python -m flask --app back_app run -h 0.0.0.0 -p 5000
