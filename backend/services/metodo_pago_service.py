from typing import List, Optional
from classes.metodo_pago import MetodoPago
from repositories.metodo_pago_repository import MetodoPagoRepository


class MetodoPagoService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = MetodoPagoRepository(db_path)

    def validate(self, obj: MetodoPago) -> None:
        if not obj.descripcion:
            raise ValueError("La descripción del método de pago es obligatoria.")
        if len(obj.descripcion) > 100:
            raise ValueError("La descripción no puede exceder los 100 caracteres.")

    def insert(self, obj: MetodoPago) -> MetodoPago:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_metodo_pago: int) -> Optional[MetodoPago]:
        return self.repository.get_by_id(id_metodo_pago)

    def update(self, obj: MetodoPago) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_metodo_pago: int) -> None:
        self.repository.delete(id_metodo_pago)

    def list_all(self) -> List[MetodoPago]:
        return self.repository.get_all()
