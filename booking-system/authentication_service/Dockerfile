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

# Копирование и установка прав для скрипта миграций
COPY ./run_migrations.sh /run_migrations.sh
RUN chmod +x /run_migrations.sh

# Открытие портов
EXPOSE 8001

# Запуск скрипта миграций при сборке контейнера
# RUN ./run_migrations.sh

# Команда по умолчанию для запуска приложения
CMD ["bash" "run_migrations.sh" && "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]