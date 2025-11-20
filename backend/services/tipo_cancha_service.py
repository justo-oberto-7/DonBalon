from typing import List, Optional
from classes.tipo_cancha import TipoCancha
from repositories.tipo_cancha_repository import TipoCanchaRepository


class TipoCanchaService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = TipoCanchaRepository(db_path)

    def insert(self, obj: TipoCancha) -> TipoCancha:
        return self.repository.create(obj)

    def get_by_id(self, id_tipo: int) -> Optional[TipoCancha]:
        return self.repository.get_by_id(id_tipo)

    def update(self, obj: TipoCancha) -> None:
        self.repository.update(obj)

    def delete(self, id_tipo: int) -> None:
        self.repository.delete(id_tipo)

    def list_all(self) -> List[TipoCancha]:
        return self.repository.get_all()
