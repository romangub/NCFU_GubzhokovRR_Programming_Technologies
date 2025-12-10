import sqlite3
import os
from typing import Optional
import threading


class DatabaseConnection:
    _instance: Optional['DatabaseConnection'] = None
    _lock = threading.Lock()

    def __init__(self, db_path: str = "company.db"):
        os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)
        self._db_path = os.path.abspath(db_path)
        self._connection = sqlite3.connect(self._db_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row

    @classmethod
    def get_instance(cls, db_path: str = "company.db") -> 'DatabaseConnection':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(db_path)
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        return self._connection

    def close_connection(self) -> None:
        if self._connection:
            self._connection.close()
            DatabaseConnection._instance = None
            self._connection = None

    @property
    def db_path(self) -> str:
        return self._db_path