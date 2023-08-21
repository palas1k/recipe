FROM python:3.10-alpine

COPY requirements.txt /temp/requirements.txt

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password wokuser
COPY wok /wok
WORKDIR /wok
EXPOSE 8000

USER wokuser