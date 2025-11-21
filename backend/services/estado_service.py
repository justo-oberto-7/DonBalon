import sqlite3
from typing import List, Optional
from classes.estado import Estado
from repositories.estado_repository import EstadoRepository


class EstadoService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = EstadoRepository(db_path, connection)

    def validate(self, obj: Estado) -> None:
        if not obj.nombre:
            raise ValueError("El nombre del estado es obligatorio.")
        if len(obj.nombre) > 50:
            raise ValueError("El nombre del estado no puede exceder los 50 caracteres.")
        if not obj.ambito:
            raise ValueError("El ámbito del estado es obligatorio.")
        if len(obj.ambito) > 50:
            raise ValueError("El ámbito del estado no puede exceder los 50 caracteres.")

    def insert(self, obj: Estado) -> Estado:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_estado: int) -> Optional[Estado]:
        return self.repository.get_by_id(id_estado)

    def update(self, obj: Estado) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_estado: int) -> None:
        self.repository.delete(id_estado)

    def list_all(self) -> List[Estado]:
        return self.repository.get_all()
