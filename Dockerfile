FROM python:3.12
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_HOME='/usr/local'
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /warehouse
COPY poetry.lock pyproject.toml /warehouse
RUN poetry install
COPY . /warehouse