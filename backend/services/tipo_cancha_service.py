from typing import List, Optional
from decimal import Decimal
from classes.tipo_cancha import TipoCancha
from repositories.tipo_cancha_repository import TipoCanchaRepository


class TipoCanchaService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = TipoCanchaRepository(db_path)

    def validate(self, obj: TipoCancha) -> None:
        if not obj.descripcion:
            raise ValueError("La descripción del tipo de cancha es obligatoria.")
        if len(obj.descripcion) > 100:
            raise ValueError("La descripción no puede exceder los 100 caracteres.")
        if not isinstance(obj.precio_hora, Decimal):
            raise ValueError("El precio por hora debe ser un Decimal.")

    def insert(self, obj: TipoCancha) -> TipoCancha:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_tipo: int) -> Optional[TipoCancha]:
        return self.repository.get_by_id(id_tipo)

    def update(self, obj: TipoCancha) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_tipo: int) -> None:
        self.repository.delete(id_tipo)

    def list_all(self) -> List[TipoCancha]:
        return self.repository.get_all()
