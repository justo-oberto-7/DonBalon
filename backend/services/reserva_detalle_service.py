from typing import List, Optional
from classes.reserva_detalle import ReservaDetalle
from repositories.reserva_detalle_repository import ReservaDetalleRepository


class ReservaDetalleService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = ReservaDetalleRepository(db_path)

    def insert(self, obj: ReservaDetalle) -> ReservaDetalle:
        return self.repository.create(obj)

    def get_by_id(self, id_detalle: int) -> Optional[ReservaDetalle]:
        return self.repository.get_by_id(id_detalle)

    def update(self, obj: ReservaDetalle) -> None:
        self.repository.update(obj)

    def delete(self, id_detalle: int) -> None:
        self.repository.delete(id_detalle)

    def list_all(self) -> List[ReservaDetalle]:
        return self.repository.get_all()
