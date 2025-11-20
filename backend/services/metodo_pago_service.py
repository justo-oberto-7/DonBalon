from typing import List, Optional
from classes.metodo_pago import MetodoPago
from repositories.metodo_pago_repository import MetodoPagoRepository


class MetodoPagoService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = MetodoPagoRepository(db_path)

    def insert(self, obj: MetodoPago) -> MetodoPago:
        return self.repository.create(obj)

    def get_by_id(self, id_metodo_pago: int) -> Optional[MetodoPago]:
        return self.repository.get_by_id(id_metodo_pago)

    def update(self, obj: MetodoPago) -> None:
        self.repository.update(obj)

    def delete(self, id_metodo_pago: int) -> None:
        self.repository.delete(id_metodo_pago)

    def list_all(self) -> List[MetodoPago]:
        return self.repository.get_all()
