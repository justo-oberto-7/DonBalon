from typing import List, Optional
from classes.pago import Pago
from repositories.pago_repository import PagoRepository


class PagoService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = PagoRepository(db_path)

    def insert(self, obj: Pago) -> Pago:
        return self.repository.create(obj)

    def get_by_id(self, id_pago: int) -> Optional[Pago]:
        return self.repository.get_by_id(id_pago)

    def update(self, obj: Pago) -> None:
        self.repository.update(obj)

    def delete(self, id_pago: int) -> None:
        self.repository.delete(id_pago)

    def list_all(self) -> List[Pago]:
        return self.repository.get_all()
