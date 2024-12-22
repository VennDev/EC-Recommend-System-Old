FROM python:3.10.2-slim-buster

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app /ai /logger /logs /utils

COPY app/ /app/
COPY ai/ /ai/
COPY logger/ /logger/
COPY utils/ /utils/
COPY requirements.txt /
COPY run_server.py /
COPY ai_config.yml /
COPY config.yml /

WORKDIR /

RUN pip3 install -r requirements.txt

ENV PYTHONPATH=/:/utils:/app:/ai:/logger

EXPOSE 5000

ENTRYPOINT ["python3", "run_server.py"]