from dataclasses import dataclass
from typing import Optional, Dict, Any
from decimal import Decimal

@dataclass
class Servicio:
    id_servicio: Optional[int] = None
    descripcion: str = ""
    costo_servicio: Decimal = Decimal("0.00")

    def to_dict(self) -> Dict[str, Any]:
        return {"id_servicio": self.id_servicio, "descripcion": self.descripcion, "costo_servicio": str(self.costo_servicio)}



def from_dict(data: Dict[str, Any]) -> "Servicio":
    costo = data.get("costo_servicio")
    costo = Decimal(str(costo)) if costo is not None else Decimal("0.00")
    return Servicio(id_servicio=data.get("id_servicio"), descripcion=data.get("descripcion", ""), costo_servicio=costo)
