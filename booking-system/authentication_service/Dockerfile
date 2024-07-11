FROM python:3.10

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание директории для приложения и установка рабочей директории
RUN mkdir /auth_app
WORKDIR /auth_app

# Копирование кода приложения
COPY . .

# Установка зависимостей Python
RUN pip install -r requirements.txt

# Открытие портов
EXPOSE 8001