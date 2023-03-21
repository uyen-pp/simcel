# syntax=docker/dockerfile:1

FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip install -r requirements.txt

COPY . .

# uvicorn cel.main:app --reload --port 10002
CMD [ "uvicorn", "main:app" , "--host", "0.0.0.0", "--port", "10002"]