from typing import List, Optional
from classes.servicio import Servicio
from repositories.servicio_repository import ServicioRepository


class ServicioService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = ServicioRepository(db_path)

    def insert(self, obj: Servicio) -> Servicio:
        return self.repository.create(obj)

    def get_by_id(self, id_servicio: int) -> Optional[Servicio]:
        return self.repository.get_by_id(id_servicio)

    def update(self, obj: Servicio) -> None:
        self.repository.update(obj)

    def delete(self, id_servicio: int) -> None:
        self.repository.delete(id_servicio)

    def list_all(self) -> List[Servicio]:
        return self.repository.get_all()
