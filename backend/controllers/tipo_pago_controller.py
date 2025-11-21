from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.tipo_pago_schema import TipoPagoCreate, TipoPagoUpdate, TipoPagoResponse
from services.tipo_pago_service import TipoPagoService
from classes.tipo_pago import TipoPago
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/tipos-pago", tags=["Tipos de Pago"])


def get_tipo_pago_service():
    """Dependency para obtener instancia de TipoPagoService"""
    db_conn = DatabaseConnection()
    return TipoPagoService(connection=db_conn.get_connection())


@router.get("/", response_model=List[TipoPagoResponse])
def list_tipos_pago(service: TipoPagoService = Depends(get_tipo_pago_service)):
    """Listar todos los tipos de pago"""
    tipos = service.list_all()
    return [TipoPagoResponse(**tipo.to_dict()) for tipo in tipos]


@router.get("/{id_tipo_pago}", response_model=TipoPagoResponse)
def get_tipo_pago(id_tipo_pago: int, service: TipoPagoService = Depends(get_tipo_pago_service)):
    """Obtener un tipo de pago por ID"""
    tipo = service.get_by_id(id_tipo_pago)
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de pago con ID {id_tipo_pago} no encontrado"
        )
    return TipoPagoResponse(**tipo.to_dict())


@router.post("/", response_model=TipoPagoResponse, status_code=status.HTTP_201_CREATED)
def create_tipo_pago(tipo_data: TipoPagoCreate, service: TipoPagoService = Depends(get_tipo_pago_service)):
    """Crear un nuevo tipo de pago"""
    # Conversión manual de Schema a Clase de Dominio
    tipo = TipoPago(
        descripcion=tipo_data.descripcion
    )
    
    try:
        created_tipo = service.insert(tipo)
        return TipoPagoResponse(**created_tipo.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_tipo_pago}", response_model=TipoPagoResponse)
def update_tipo_pago(id_tipo_pago: int, tipo_data: TipoPagoUpdate, service: TipoPagoService = Depends(get_tipo_pago_service)):
    """Actualizar un tipo de pago existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    tipo_actual = service.get_by_id(id_tipo_pago)
    if not tipo_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de pago con ID {id_tipo_pago} no encontrado"
        )
    
    # 2. Merge inteligente
    nueva_descripcion = tipo_data.descripcion if tipo_data.descripcion is not None else tipo_actual.descripcion

    # 3. Crear la instancia para actualizar con los datos mezclados
    tipo_a_guardar = TipoPago(
        id_tipo_pago=id_tipo_pago,
        descripcion=nueva_descripcion
    )
    
    try:
        service.update(tipo_a_guardar)
        return TipoPagoResponse(**tipo_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_tipo_pago}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipo_pago(id_tipo_pago: int, service: TipoPagoService = Depends(get_tipo_pago_service)):
    """Eliminar un tipo de pago"""
    existing = service.get_by_id(id_tipo_pago)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de pago con ID {id_tipo_pago} no encontrado"
        )
    
    service.delete(id_tipo_pago)
    return None
