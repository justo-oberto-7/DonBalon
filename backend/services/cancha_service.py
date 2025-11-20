from typing import List, Optional
from classes.cancha import Cancha
from repositories.cancha_repository import CanchaRepository


class CanchaService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = CanchaRepository(db_path)

    def insert(self, obj: Cancha) -> Cancha:
        return self.repository.create(obj)

    def get_by_id(self, id_cancha: int) -> Optional[Cancha]:
        return self.repository.get_by_id(id_cancha)

    def update(self, obj: Cancha) -> None:
        self.repository.update(obj)

    def delete(self, id_cancha: int) -> None:
        self.repository.delete(id_cancha)

    def list_all(self) -> List[Cancha]:
        return self.repository.get_all()
