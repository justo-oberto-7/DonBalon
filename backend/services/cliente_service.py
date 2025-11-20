from typing import List, Optional
from classes.cliente import Cliente
from repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self, db_path: Optional[str] = None):
        self.repository = ClienteRepository(db_path)

    def insert(self, cliente: Cliente) -> Cliente:
        return self.repository.create(cliente)

    def get_by_id(self, id_cliente: int) -> Optional[Cliente]:
        return self.repository.get_by_id(id_cliente)

    def update(self, cliente: Cliente) -> None:
        self.repository.update(cliente)

    def delete(self, id_cliente: int) -> None:
        self.repository.delete(id_cliente)

    def list_all(self) -> List[Cliente]:
        return self.repository.get_all()
