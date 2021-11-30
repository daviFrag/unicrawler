# syntax=docker/dockerfile:1
FROM python:3.10.0

WORKDIR /bot

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt && mkdir cache

COPY . /bot

CMD ["python", "bot.py"]