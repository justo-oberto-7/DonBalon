from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ReservaDetalleBase(BaseModel):
    id_reserva: int = Field(..., description="ID de la reserva")
    id_turno: int = Field(..., description="ID del turno")
    precio_total_item: Decimal = Field(..., description="Precio total del item")


class ReservaDetalleCreate(ReservaDetalleBase):
    pass


class ReservaDetalleUpdate(BaseModel):
    id_reserva: Optional[int] = None
    id_turno: Optional[int] = None
    precio_total_item: Optional[Decimal] = None


class ReservaDetalleResponse(ReservaDetalleBase):
    id_detalle: int

    class Config:
        from_attributes = True
