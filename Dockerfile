FROM python:3.11-alpine
USER root
RUN mkdir -p /pump_up_your_ass
WORKDIR /pump_up_your_ass
COPY requirements.txt /pump_up_your_ass
RUN apk update &&\
    apk add py3-pip cmake curl python3-dev libpq-dev gcc ca-certificates musl-dev libc-dev --no-cache &&\
    pip install --no-cache-dir --upgrade pip setuptools wheel &&\
    pip install --no-cache-dir -r requirements.txt
EXPOSE 8010
CMD python3 main.py
