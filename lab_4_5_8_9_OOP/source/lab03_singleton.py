# source/lab03_singleton.py

import sqlite3
import os
from typing import Optional
import threading


class DatabaseConnection:
    _instances: dict[str, 'DatabaseConnection'] = {}  # ключ — нормализованный путь
    _lock = threading.Lock()

    def __init__(self, db_path: str = "company.db"):
        # Этот метод будет вызываться только при создании нового экземпляра
        normalized_path = os.path.abspath(db_path)
        os.makedirs(os.path.dirname(normalized_path) or '.', exist_ok=True)
        
        self._db_path = normalized_path
        self._connection = sqlite3.connect(self._db_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row

    @classmethod
    def get_instance(cls, db_path: str = "company.db") -> 'DatabaseConnection':
        normalized_path = os.path.abspath(db_path)
        
        if normalized_path not in cls._instances:
            with cls._lock:
                if normalized_path not in cls._instances:
                    # Создаём новый экземпляр только если его ещё нет
                    cls._instances[normalized_path] = cls(db_path)
        
        return cls._instances[normalized_path]

    def get_connection(self) -> sqlite3.Connection:
        return self._connection

    def close_connection(self) -> None:
        if self._connection:
            self._connection.close()
            # Удаляем из словаря, чтобы при следующем get_instance создался новый
            if self._db_path in self._instances:
                del self._instances[self._db_path]

    @property
    def db_path(self) -> str:
        return self._db_path