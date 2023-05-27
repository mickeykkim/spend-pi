ARG PYTHON_BASE

FROM python:${PYTHON_BASE} as base
ARG PYPI_URL

RUN mkdir /api
WORKDIR /spend_pi

# copy build files
COPY pyproject.toml poetry.lock README.rst /spend_pi/
COPY api /spend_pi/spend_pi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    PIP_INDEX_URL=$PYPI_URL

RUN apt-get update -qq && apt-get install -qqy -f \
    build-essential \
    && pip install -Iv --prefer-binary --index-url $PYPI_URL --upgrade \
    pip \
    poetry==1.4.3

RUN poetry install --only main

FROM base as test
ARG PYPI_URL

WORKDIR /spend_pi
COPY tests /spend_pi/tests

# required to make sure pytest runs the right coverage checks
ENV PYTHONPATH .

# Must reinstall certain packages after poetry install --no-dev See: https://github.com/python-poetry/poetry/issues/4463
RUN pip install -Iv --prefer-binary --index-url $PYPI_URL --upgrade \
    pip \
    tomlkit \
    virtualenv \
    requests \
    && poetry install
