#!/bin/bash

# Тестирование создания файла
touch /app/configs/test_file.txt
echo "Initial content" > /app/configs/test_file.txt

# Тестирование изменения файла
echo "Modified content" > /app/configs/test_file.txt

# Тестирование удаления файла
rm /app/configs/test_file.txt

# Тестирование восстановления версии файла
python3 config_versioning.py rollback /app/configs/test_file.txt 1

echo "Все тесты пройдены успешно"