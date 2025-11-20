from typing import List, Optional
from classes.torneo import Torneo
from repositories.torneo_repository import TorneoRepository


class TorneoService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = TorneoRepository(db_path)

    def insert(self, obj: Torneo) -> Torneo:
        return self.repository.create(obj)

    def get_by_id(self, id_torneo: int) -> Optional[Torneo]:
        return self.repository.get_by_id(id_torneo)

    def update(self, obj: Torneo) -> None:
        self.repository.update(obj)

    def delete(self, id_torneo: int) -> None:
        self.repository.delete(id_torneo)

    def list_all(self) -> List[Torneo]:
        return self.repository.get_all()
