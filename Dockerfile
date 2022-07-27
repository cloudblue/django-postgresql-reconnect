ARG  PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}

WORKDIR /app

ADD . /app

RUN pip install poetry && poetry install
