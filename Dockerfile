# syntax=docker/dockerfile:1
FROM python:3.10.0

WORKDIR /bot

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . /bot

CMD ["python", "bot.py"]