# Dockerfile

# pull the official docker image
FROM python:3.10.12-slim

# set work directory
RUN mkdir /backend
WORKDIR /backend

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./backend/requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /backend/requirements.txt

EXPOSE 8000

CMD uvicorn backend.main:app --host 0.0.0.0 --reload