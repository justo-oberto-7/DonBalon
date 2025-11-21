from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.reserva_detalle_schema import ReservaDetalleCreate, ReservaDetalleUpdate, ReservaDetalleResponse
from services.reserva_detalle_service import ReservaDetalleService
from classes.reserva_detalle import ReservaDetalle
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/reservas-detalles", tags=["Reservas Detalles"])


def get_reserva_detalle_service():
    """Dependency para obtener instancia de ReservaDetalleService"""
    db_conn = DatabaseConnection()
    return ReservaDetalleService(connection=db_conn.get_connection())


@router.get("/", response_model=List[ReservaDetalleResponse])
def list_reservas_detalles(service: ReservaDetalleService = Depends(get_reserva_detalle_service)):
    """Listar todos los detalles de reservas"""
    detalles = service.list_all()
    return [ReservaDetalleResponse(**detalle.to_dict()) for detalle in detalles]


@router.get("/{id_detalle}", response_model=ReservaDetalleResponse)
def get_reserva_detalle(id_detalle: int, service: ReservaDetalleService = Depends(get_reserva_detalle_service)):
    """Obtener un detalle de reserva por ID"""
    detalle = service.get_by_id(id_detalle)
    if not detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Detalle de reserva con ID {id_detalle} no encontrado"
        )
    return ReservaDetalleResponse(**detalle.to_dict())


@router.post("/", response_model=ReservaDetalleResponse, status_code=status.HTTP_201_CREATED)
def create_reserva_detalle(detalle_data: ReservaDetalleCreate, service: ReservaDetalleService = Depends(get_reserva_detalle_service)):
    """Crear un nuevo detalle de reserva"""
    # Conversión manual de Schema a Clase de Dominio
    detalle = ReservaDetalle(
        id_reserva=detalle_data.id_reserva,
        id_cancha=detalle_data.id_cancha,
        id_horario=detalle_data.id_horario,
        precioxhora=detalle_data.precioxhora,
        costoxhora=detalle_data.costoxhora,
        precio_total_item=detalle_data.precio_total_item
    )
    
    try:
        created_detalle = service.insert(detalle)
        return ReservaDetalleResponse(**created_detalle.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_detalle}", response_model=ReservaDetalleResponse)
def update_reserva_detalle(id_detalle: int, detalle_data: ReservaDetalleUpdate, service: ReservaDetalleService = Depends(get_reserva_detalle_service)):
    """Actualizar un detalle de reserva existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    detalle_actual = service.get_by_id(id_detalle)
    if not detalle_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Detalle de reserva con ID {id_detalle} no encontrado"
        )
    
    # 2. Merge inteligente
    nueva_reserva = detalle_data.id_reserva if detalle_data.id_reserva is not None else detalle_actual.id_reserva
    nueva_cancha = detalle_data.id_cancha if detalle_data.id_cancha is not None else detalle_actual.id_cancha
    nuevo_horario = detalle_data.id_horario if detalle_data.id_horario is not None else detalle_actual.id_horario
    nuevo_precio_hora = detalle_data.precioxhora if detalle_data.precioxhora is not None else detalle_actual.precioxhora
    nuevo_costo_hora = detalle_data.costoxhora if detalle_data.costoxhora is not None else detalle_actual.costoxhora
    nuevo_precio_total = detalle_data.precio_total_item if detalle_data.precio_total_item is not None else detalle_actual.precio_total_item

    # 3. Crear la instancia para actualizar con los datos mezclados
    detalle_a_guardar = ReservaDetalle(
        id_detalle=id_detalle,
        id_reserva=nueva_reserva,
        id_cancha=nueva_cancha,
        id_horario=nuevo_horario,
        precioxhora=nuevo_precio_hora,
        costoxhora=nuevo_costo_hora,
        precio_total_item=nuevo_precio_total
    )
    
    try:
        service.update(detalle_a_guardar)
        return ReservaDetalleResponse(**detalle_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_detalle}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reserva_detalle(id_detalle: int, service: ReservaDetalleService = Depends(get_reserva_detalle_service)):
    """Eliminar un detalle de reserva"""
    existing = service.get_by_id(id_detalle)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Detalle de reserva con ID {id_detalle} no encontrado"
        )
    
    service.delete(id_detalle)
    return None
