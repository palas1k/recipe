FROM python:3.10-alpine3.18

COPY requirements.txt /temp/requirements.txt

RUN pip install -r temp/requirements.txt

COPY wok /wok
WORKDIR /wok
EXPOSE 8000

RUN adduser --disabled-password wokuser

USER wokuser