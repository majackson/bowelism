FROM python:3.13
ENV PYTHONUNBUFFERED 1

# install packages
RUN apt-get update
RUN pip install virtualenv

RUN mkdir /code
WORKDIR /code

ADD . /code/

RUN python3 -m venv ~/.venvs/bowelismvenv && \
    . ~/.venvs/bowelismvenv/bin/activate && \
    pip install -r requirements.txt && \
    pip install -r dev_requirements.txt

