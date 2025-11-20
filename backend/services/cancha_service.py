from typing import List, Optional
from classes.cancha import Cancha
from repositories.cancha_repository import CanchaRepository


class CanchaService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = CanchaRepository(db_path)

    def validate(self, obj: Cancha) -> None:
        if not obj.nombre:
            raise ValueError("El nombre de la cancha es obligatorio.")
        if len(obj.nombre) > 100:
            raise ValueError("El nombre de la cancha no puede exceder los 100 caracteres.")
        if not isinstance(obj.id_estado, int):
            raise ValueError("El id_estado debe ser un entero.")
        if not isinstance(obj.id_tipo, int):
            raise ValueError("El id_tipo debe ser un entero.")

    def insert(self, obj: Cancha) -> Cancha:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_cancha: int) -> Optional[Cancha]:
        return self.repository.get_by_id(id_cancha)

    def update(self, obj: Cancha) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_cancha: int) -> None:
        self.repository.delete(id_cancha)

    def list_all(self) -> List[Cancha]:
        return self.repository.get_all()
