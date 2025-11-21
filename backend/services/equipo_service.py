import sqlite3
from typing import List, Optional
from classes.equipo import Equipo
from repositories.equipo_repository import EquipoRepository


class EquipoService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = EquipoRepository(db_path, connection)

    def validate(self, obj: Equipo) -> None:
        if not obj.nombre:
            raise ValueError("El nombre del equipo es obligatorio.")
        if len(obj.nombre) > 50:
            raise ValueError("El nombre del equipo no puede exceder los 50 caracteres.")
        if not isinstance(obj.cant_jugadores, int):
            raise ValueError("La cantidad de jugadores debe ser un entero.")
        if not isinstance(obj.id_torneo, int):
            raise ValueError("El id_torneo debe ser un entero.")

    def insert(self, obj: Equipo) -> Equipo:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_equipo: int) -> Optional[Equipo]:
        return self.repository.get_by_id(id_equipo)

    def update(self, obj: Equipo) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_equipo: int) -> None:
        self.repository.delete(id_equipo)

    def list_all(self) -> List[Equipo]:
        return self.repository.get_all()

    def get_by_torneo(self, id_torneo: int) -> List[Equipo]:
        return self.repository.get_by_torneo(id_torneo)
