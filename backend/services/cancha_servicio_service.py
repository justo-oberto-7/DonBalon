import sqlite3
from typing import List, Optional
from classes.cancha_servicio import CanchaServicio
from repositories.cancha_servicio_repository import CanchaServicioRepository


class CanchaServicioService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = CanchaServicioRepository(db_path, connection)

    def validate(self, obj: CanchaServicio) -> None:
        if not isinstance(obj.id_cancha, int):
            raise ValueError("El id_cancha debe ser un entero.")
        if not isinstance(obj.id_servicio, int):
            raise ValueError("El id_servicio debe ser un entero.")

    def insert(self, obj: CanchaServicio) -> CanchaServicio:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_ids(self, id_cancha: int, id_servicio: int) -> Optional[CanchaServicio]:
        return self.repository.get_by_ids(id_cancha, id_servicio)

    def delete(self, id_cancha: int, id_servicio: int) -> None:
        self.repository.delete(id_cancha, id_servicio)

    def list_all(self) -> List[CanchaServicio]:
        return self.repository.get_all()

