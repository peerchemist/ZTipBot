FROM python:3.8-slim

COPY requirements.txt /

RUN pip3 install --no-cache-dir -r /requirements.txt

COPY src/ /src
WORKDIR /src

ENV APP_ENV docker

CMD ["python3" "bot.py"]