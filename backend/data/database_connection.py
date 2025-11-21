import sqlite3
import os
from typing import Optional

class DatabaseConnection:
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[sqlite3.Connection] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance

    def _initialize_connection(self):
        """Inicializa la conexión a la base de datos."""
        if self._connection is None:
            # Obtener la ruta al archivo donbalon.db en la carpeta backend/data
            # Este archivo está en backend/data/database_connection.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, "donbalon.db")
            
            self._connection = sqlite3.connect(db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")

    def get_connection(self) -> sqlite3.Connection:
        """Retorna la conexión activa."""
        if self._connection is None:
            self._initialize_connection()
        return self._connection

    def close(self):
        """Cierra la conexión explícitamente. Usar solo al apagar la app."""
        if self._connection:
            self._connection.close()
            self._connection = None
