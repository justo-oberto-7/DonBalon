from typing import List, Optional
from classes.cancha_servicio import CanchaServicio
from repositories.cancha_servicio_repository import CanchaServicioRepository


class CanchaServicioService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = CanchaServicioRepository(db_path)

    def insert(self, obj: CanchaServicio) -> CanchaServicio:
        return self.repository.create(obj)

    def get_by_id(self, id_cancha: int, id_servicio: int) -> Optional[CanchaServicio]:
        return self.repository.get_by_ids(id_cancha, id_servicio)

    def delete(self, id_cancha: int, id_servicio: int) -> None:
        self.repository.delete(id_cancha, id_servicio)

    def list_all(self) -> List[CanchaServicio]:
        return self.repository.get_all()
