FROM python:3.7-alpine

WORKDIR /code

ENV FLASK_APP=./src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=1
ENV FLASK_DATA_PATH /data/TESTDATEI.txt


COPY . .

RUN apk add --no-cache \
                    gcc \
                    musl-dev \
                    linux-headers \
                    postgresql-dev && \
    pip install --upgrade pip && \
    pip install -r ./src/requirements.txt


CMD ["flask", "run"]
