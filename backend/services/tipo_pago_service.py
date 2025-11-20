from typing import List, Optional
from classes.tipo_pago import TipoPago
from repositories.tipo_pago_repository import TipoPagoRepository


class TipoPagoService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = TipoPagoRepository(db_path)

    def insert(self, obj: TipoPago) -> TipoPago:
        return self.repository.create(obj)

    def get_by_id(self, id_tipo_pago: int) -> Optional[TipoPago]:
        return self.repository.get_by_id(id_tipo_pago)

    def update(self, obj: TipoPago) -> None:
        self.repository.update(obj)

    def delete(self, id_tipo_pago: int) -> None:
        self.repository.delete(id_tipo_pago)

    def list_all(self) -> List[TipoPago]:
        return self.repository.get_all()
