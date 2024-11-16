import os
import time
import sqlite3
import hashlib
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Настройки
CONFIG_DIR = "/app/configs"
DB_PATH = "/app/config_versions.db"

# Создание базы данных и таблиц
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT,
            version_hash TEXT,
            timestamp TEXT,
            author TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

# Хранение версии файла
def store_version(file_path, author, description=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO versions (file_path, version_hash, timestamp, author, description)
        VALUES (?, ?, ?, ?, ?)
    """, (file_path, file_hash, timestamp, author, description))
    conn.commit()
    conn.close()

# Получение истории версий файла
def get_history(file_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM versions WHERE file_path = ? ORDER BY timestamp DESC
    """, (file_path,))
    history = cursor.fetchall()
    conn.close()
    return history

# Откат к предыдущей версии файла
def rollback(file_path, version_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT version_hash FROM versions WHERE id = ?
    """, (version_id,))
    version_hash = cursor.fetchone()[0]
    cursor.execute("""
        SELECT version_hash FROM versions WHERE file_path = ? ORDER BY timestamp DESC
    """, (file_path,))
    current_hash = cursor.fetchone()[0]
    if version_hash == current_hash:
        print("Файл уже находится в указанной версии")
        return
    cursor.execute("""
        SELECT timestamp FROM versions WHERE id = ?
    """, (version_id,))
    timestamp = cursor.fetchone()[0]
    cursor.execute("""
        SELECT version_hash FROM versions WHERE file_path = ? AND timestamp < ? ORDER BY timestamp DESC
    """, (file_path, timestamp))
    previous_hash = cursor.fetchone()[0]
    with open(file_path, 'rb') as f:
        current_content = f.read()
    if hashlib.md5(current_content).hexdigest() == previous_hash:
        print("Файл уже находится в указанной версии")
        return
    cursor.execute("""
        SELECT version_hash FROM versions WHERE file_path = ? AND timestamp >= ? ORDER BY timestamp ASC
    """, (file_path, timestamp))
    versions = cursor.fetchall()
    for version in versions:
        with open(file_path, 'rb') as f:
            content = f.read()
        if hashlib.md5(content).hexdigest() == version[0]:
            with open(file_path, 'wb') as f:
                f.write(content)
            print(f"Версия файла {file_path} восстановлена до {timestamp}")
            return
    print("Не удалось восстановить версию файла")

# Обработчик событий файловой системы
class ConfigHandler(FileSystemEventHandler):
    def __init__(self, author):
        self.author = author

    def on_modified(self, event):
        if event.is_directory:
            return
        store_version(event.src_path, self.author)

    def on_created(self, event):
        if event.is_directory:
            return
        store_version(event.src_path, self.author)

    def on_deleted(self, event):
        if event.is_directory:
            return
        store_version(event.src_path, self.author, description="Файл удален")

# Основная функция
def main():
    init_db()
    author = os.getlogin()
    event_handler = ConfigHandler(author)
    observer = Observer()
    observer.schedule(event_handler, path=CONFIG_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()