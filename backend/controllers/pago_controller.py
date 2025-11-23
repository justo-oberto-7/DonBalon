from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.pago_schema import PagoCreate, PagoUpdate, PagoResponse
from services.pago_service import PagoService
from classes.pago import Pago
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/pagos", tags=["Pagos"])


def get_pago_service():
    """Dependency para obtener instancia de PagoService"""
    db_conn = DatabaseConnection()
    return PagoService(connection=db_conn.get_connection())


@router.get("/", response_model=List[PagoResponse])
def list_pagos(service: PagoService = Depends(get_pago_service)):
    """Listar todos los pagos"""
    pagos = service.list_all()
    return [PagoResponse(**pago.to_dict()) for pago in pagos]


@router.get("/{id_pago}", response_model=PagoResponse)
def get_pago(id_pago: int, service: PagoService = Depends(get_pago_service)):
    """Obtener un pago por ID"""
    pago = service.get_by_id(id_pago)
    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pago con ID {id_pago} no encontrado"
        )
    return PagoResponse(**pago.to_dict())


@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def create_pago(pago_data: PagoCreate, service: PagoService = Depends(get_pago_service)):
    """Crear un nuevo pago"""
    # Conversión manual de Schema a Clase de Dominio
    pago = Pago(
        id_reserva=pago_data.id_reserva,
        id_metodo_pago=pago_data.id_metodo_pago,
        fecha_pago=pago_data.fecha_pago,
        monto=pago_data.monto
    )
    
    try:
        created_pago = service.insert(pago)
        return PagoResponse(**created_pago.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_pago}", response_model=PagoResponse)
def update_pago(id_pago: int, pago_data: PagoUpdate, service: PagoService = Depends(get_pago_service)):
    """Actualizar un pago existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    pago_actual = service.get_by_id(id_pago)
    if not pago_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pago con ID {id_pago} no encontrado"
        )
    
    # 2. Merge inteligente
    nueva_reserva = pago_data.id_reserva if pago_data.id_reserva is not None else pago_actual.id_reserva
    nuevo_metodo = pago_data.id_metodo_pago if pago_data.id_metodo_pago is not None else pago_actual.id_metodo_pago
    nueva_fecha = pago_data.fecha_pago if pago_data.fecha_pago is not None else pago_actual.fecha_pago
    nuevo_monto = pago_data.monto if pago_data.monto is not None else pago_actual.monto

    # 3. Crear la instancia para actualizar con los datos mezclados
    pago_a_guardar = Pago(
        id_pago=id_pago,
        id_reserva=nueva_reserva,
        id_metodo_pago=nuevo_metodo,
        fecha_pago=nueva_fecha,
        monto=nuevo_monto
    )
    
    try:
        service.update(pago_a_guardar)
        return PagoResponse(**pago_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_pago}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pago(id_pago: int, service: PagoService = Depends(get_pago_service)):
    """Eliminar un pago"""
    existing = service.get_by_id(id_pago)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pago con ID {id_pago} no encontrado"
        )
    
    service.delete(id_pago)
    return None
