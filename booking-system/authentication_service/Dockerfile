FROM python:3.10

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /auth_app
WORKDIR /auth_app

COPY . .

RUN pip install -r requirements.txt


EXPOSE 8001