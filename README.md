# Система контроля версий для конфигурационных файлов

## Установка и запуск

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/config_versioning.git
    cd config_versioning
    ```

2. Соберите и запустите контейнер:

    ```bash
    ./build_and_run.sh
    ```

## Ручной запуск

1. Активируйте виртуальное окружение:

    ```bash
    source config_versioning_env/bin/activate
    ```

2. Запустите скрипт для отслеживания изменений:

    ```bash
    python3 config_versioning.py
    ```

## Тестирование

1. Запустите скрипт для автоматического тестирования:

    ```bash
    ./test_script.sh
    ```

## Зависимости

- Python 3.12
- watchdog
- SQLite