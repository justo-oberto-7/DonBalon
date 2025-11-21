import sqlite3
from typing import List, Optional
from decimal import Decimal
from classes.pago import Pago
from repositories.pago_repository import PagoRepository


class PagoService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = PagoRepository(db_path, connection)

    def validate(self, obj: Pago) -> None:
        if not isinstance(obj.id_reserva, int):
            raise ValueError("El id_reserva debe ser un entero.")
        if not isinstance(obj.id_metodo_pago, int):
            raise ValueError("El id_metodo_pago debe ser un entero.")
        if not obj.fecha_pago:
            raise ValueError("La fecha de pago es obligatoria.")
        if not isinstance(obj.monto, Decimal):
            raise ValueError("El monto debe ser un Decimal.")
        if not obj.estado_pago:
            raise ValueError("El estado del pago es obligatorio.")
        if len(obj.estado_pago) > 30:
            raise ValueError("El estado del pago no puede exceder los 30 caracteres.")

    def insert(self, obj: Pago) -> Pago:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_pago: int) -> Optional[Pago]:
        return self.repository.get_by_id(id_pago)

    def update(self, obj: Pago) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_pago: int) -> None:
        self.repository.delete(id_pago)

    def list_all(self) -> List[Pago]:
        return self.repository.get_all()
