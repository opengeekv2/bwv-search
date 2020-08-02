FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.lock.txt /code/
RUN apt-get update
RUN apt-get install -y musescore xvfb python3-pygame
RUN pip install --upgrade pip
RUN pip install -r requirements.lock.txt
COPY . /code/