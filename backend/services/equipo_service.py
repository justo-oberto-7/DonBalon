from typing import List, Optional
from classes.equipo import Equipo
from repositories.equipo_repository import EquipoRepository


class EquipoService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = EquipoRepository(db_path)

    def insert(self, obj: Equipo) -> Equipo:
        return self.repository.create(obj)

    def get_by_id(self, id_equipo: int) -> Optional[Equipo]:
        return self.repository.get_by_id(id_equipo)

    def update(self, obj: Equipo) -> None:
        self.repository.update(obj)

    def delete(self, id_equipo: int) -> None:
        self.repository.delete(id_equipo)

    def list_all(self) -> List[Equipo]:
        return self.repository.get_all()

    def get_by_torneo(self, id_torneo: int) -> List[Equipo]:
        return self.repository.get_by_torneo(id_torneo)
