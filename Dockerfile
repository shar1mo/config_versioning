# Используем базовый образ с Python
FROM python:3.12-slim

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Копируем исходники в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install watchdog

# Указываем рабочую директорию
WORKDIR /app

# Команда для запуска скрипта
CMD ["./build_and_run.sh"]