FROM python:3.10

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание директории для приложения и установка рабочей директории
RUN mkdir /notification_app
WORKDIR /notification_app

# Копирование кода приложения
COPY . .

# Установка зависимостей Python
RUN pip install -r requirements.txt


# Запуск скрипта миграций при сборке контейнера
# RUN ./run_migrations.sh

# Команда по умолчанию для запуска приложения
CMD ["python", "messaging/consumer.py"]