FROM python:3.10-slim

COPY requirements.txt /

RUN pip3 install --no-cache-dir -r /requirements.txt

COPY src/ /app
WORKDIR /app

ENV APP_ENV docker

CMD ["python3", "bot.py"]
