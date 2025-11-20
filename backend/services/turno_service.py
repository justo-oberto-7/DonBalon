from typing import List, Optional
from classes.turno import Turno
from repositories.turno_repository import TurnoRepository


class TurnoService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = TurnoRepository(db_path)

    def insert(self, obj: Turno) -> Turno:
        return self.repository.create(obj)

    def get_by_id(self, id_turno: int) -> Optional[Turno]:
        return self.repository.get_by_id(id_turno)

    def update(self, obj: Turno) -> None:
        self.repository.update(obj)

    def delete(self, id_turno: int) -> None:
        self.repository.delete(id_turno)

    def list_all(self) -> List[Turno]:
        return self.repository.get_all()
