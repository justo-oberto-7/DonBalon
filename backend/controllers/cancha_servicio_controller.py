from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.cancha_servicio_schema import CanchaServicioCreate, CanchaServicioResponse
from services.cancha_servicio_service import CanchaServicioService
from classes.cancha_servicio import CanchaServicio
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/canchas-servicios", tags=["Canchas-Servicios"])


def get_cancha_servicio_service():
    """Dependency para obtener instancia de CanchaServicioService"""
    db_conn = DatabaseConnection()
    return CanchaServicioService(connection=db_conn.get_connection())


@router.get("/", response_model=List[CanchaServicioResponse])
def list_canchas_servicios(service: CanchaServicioService = Depends(get_cancha_servicio_service)):
    """Listar todas las relaciones cancha-servicio"""
    items = service.list_all()
    return [CanchaServicioResponse(**item.to_dict()) for item in items]


@router.get("/cancha/{id_cancha}", response_model=List[CanchaServicioResponse])
def get_by_cancha(id_cancha: int, service: CanchaServicioService = Depends(get_cancha_servicio_service)):
    """Obtener servicios por ID de cancha"""
    items = service.list_all()
    filtered = [item for item in items if item.id_cancha == id_cancha]
    return [CanchaServicioResponse(**item.to_dict()) for item in filtered]


@router.post("/", response_model=CanchaServicioResponse, status_code=status.HTTP_201_CREATED)
def create_cancha_servicio(data: CanchaServicioCreate, service: CanchaServicioService = Depends(get_cancha_servicio_service)):
    """Crear una nueva relación cancha-servicio"""
    # Conversión manual de Schema a Clase de Dominio
    cancha_servicio = CanchaServicio(
        id_cancha=data.id_cancha,
        id_servicio=data.id_servicio
    )
    
    try:
        created = service.insert(cancha_servicio)
        return CanchaServicioResponse(**created.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/cancha/{id_cancha}/servicio/{id_servicio}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cancha_servicio(id_cancha: int, id_servicio: int, service: CanchaServicioService = Depends(get_cancha_servicio_service)):
    """Eliminar una relación cancha-servicio"""
    # Buscar la relación
    items = service.list_all()
    found = None
    for item in items:
        if item.id_cancha == id_cancha and item.id_servicio == id_servicio:
            found = item
            break
    
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Relación cancha-servicio no encontrada"
        )
    
    service.delete(id_cancha, id_servicio)
    return None
