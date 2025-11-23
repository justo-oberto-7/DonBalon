import sqlite3
import os
from pathlib import Path

def init_database(db_path=None):
    """
    Inicializa la base de datos SQLite con el esquema definido en database.sql
    
    Args:
        db_path (str): Ruta a la base de datos. Si es None, se crea en la carpeta actual.
    """
    if db_path is None:
        # Crear la BD en la carpeta backend/data
        current_dir = Path(__file__).parent
        db_path = current_dir / "donbalon.db"
    else:
        db_path = Path(db_path)
    
    # Leer el archivo SQL
    sql_file = Path(__file__).parent / "database.sql"
    
    if not sql_file.exists():
        raise FileNotFoundError(f"No se encontró el archivo SQL en {sql_file}")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Crear la conexión
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Ejecutar el script SQL
        cursor.executescript(sql_script)
        conn.commit()
        print(f" Base de datos creada exitosamente en: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f" Error al crear la base de datos: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    # Crear la BD en la carpeta backend/data
    data_dir = Path(__file__).parent
    db_path = data_dir / "donbalon.db"
    
    # Eliminar la BD anterior si existe
    #if db_path.exists():
    #    os.remove(db_path)
    #    print("BD anterior eliminada")
    
    # Inicializar la BD
    init_database(str(db_path))
    
    print("\n Base de datos lista para usar!")
    print(f"Ubicación: {db_path}")
