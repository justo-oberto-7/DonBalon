from typing import List, Optional
from classes.estado import Estado
from repositories.estado_repository import EstadoRepository


class EstadoService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = EstadoRepository(db_path)

    def insert(self, obj: Estado) -> Estado:
        return self.repository.create(obj)

    def get_by_id(self, id_estado: int) -> Optional[Estado]:
        return self.repository.get_by_id(id_estado)

    def update(self, obj: Estado) -> None:
        self.repository.update(obj)

    def delete(self, id_estado: int) -> None:
        self.repository.delete(id_estado)

    def list_all(self) -> List[Estado]:
        return self.repository.get_all()
