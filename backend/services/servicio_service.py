import sqlite3
from typing import List, Optional
from decimal import Decimal
from classes.servicio import Servicio
from repositories.servicio_repository import ServicioRepository


class ServicioService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = ServicioRepository(db_path, connection)

    def validate(self, obj: Servicio) -> None:
        if not obj.descripcion:
            raise ValueError("La descripción del servicio es obligatoria.")
        if len(obj.descripcion) > 100:
            raise ValueError("La descripción no puede exceder los 100 caracteres.")
        if not isinstance(obj.costoxservicio, Decimal):
            raise ValueError("El costo del servicio debe ser un Decimal.")

    def insert(self, obj: Servicio) -> Servicio:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_servicio: int) -> Optional[Servicio]:
        return self.repository.get_by_id(id_servicio)

    def update(self, obj: Servicio) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_servicio: int) -> None:
        self.repository.delete(id_servicio)

    def list_all(self) -> List[Servicio]:
        return self.repository.get_all()
