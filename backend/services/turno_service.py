from typing import List, Optional
from classes.turno import Turno
from repositories.turno_repository import TurnoRepository


class TurnoService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = TurnoRepository(db_path)

    def validate(self, obj: Turno) -> None:
        if not isinstance(obj.id_cancha, int):
            raise ValueError("El id_cancha debe ser un entero.")
        if not isinstance(obj.id_horario, int):
            raise ValueError("El id_horario debe ser un entero.")
        if not obj.fecha:
            raise ValueError("La fecha es obligatoria.")

    def insert(self, obj: Turno) -> Turno:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_turno: int) -> Optional[Turno]:
        return self.repository.get_by_id(id_turno)

    def update(self, obj: Turno) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_turno: int) -> None:
        self.repository.delete(id_turno)

    def list_all(self) -> List[Turno]:
        return self.repository.get_all()
