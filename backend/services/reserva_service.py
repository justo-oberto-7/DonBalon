from typing import List, Optional
from classes.reserva import Reserva
from repositories.reserva_repository import ReservaRepository


class ReservaService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = ReservaRepository(db_path)

    def insert(self, obj: Reserva) -> Reserva:
        return self.repository.create(obj)

    def get_by_id(self, id_reserva: int) -> Optional[Reserva]:
        return self.repository.get_by_id(id_reserva)

    def update(self, obj: Reserva) -> None:
        self.repository.update(obj)

    def delete(self, id_reserva: int) -> None:
        self.repository.delete(id_reserva)

    def list_all(self) -> List[Reserva]:
        return self.repository.get_all()
