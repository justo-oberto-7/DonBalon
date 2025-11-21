from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.metodo_pago_schema import MetodoPagoCreate, MetodoPagoUpdate, MetodoPagoResponse
from services.metodo_pago_service import MetodoPagoService
from classes.metodo_pago import MetodoPago
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/metodos-pago", tags=["Métodos de Pago"])


def get_metodo_pago_service():
    """Dependency para obtener instancia de MetodoPagoService"""
    db_conn = DatabaseConnection()
    return MetodoPagoService(connection=db_conn.get_connection())


@router.get("/", response_model=List[MetodoPagoResponse])
def list_metodos_pago(service: MetodoPagoService = Depends(get_metodo_pago_service)):
    """Listar todos los métodos de pago"""
    metodos = service.list_all()
    return [MetodoPagoResponse(**metodo.to_dict()) for metodo in metodos]


@router.get("/{id_metodo_pago}", response_model=MetodoPagoResponse)
def get_metodo_pago(id_metodo_pago: int, service: MetodoPagoService = Depends(get_metodo_pago_service)):
    """Obtener un método de pago por ID"""
    metodo = service.get_by_id(id_metodo_pago)
    if not metodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Método de pago con ID {id_metodo_pago} no encontrado"
        )
    return MetodoPagoResponse(**metodo.to_dict())


@router.post("/", response_model=MetodoPagoResponse, status_code=status.HTTP_201_CREATED)
def create_metodo_pago(metodo_data: MetodoPagoCreate, service: MetodoPagoService = Depends(get_metodo_pago_service)):
    """Crear un nuevo método de pago"""
    # Conversión manual de Schema a Clase de Dominio
    metodo = MetodoPago(
        descripcion=metodo_data.descripcion
    )
    
    try:
        created_metodo = service.insert(metodo)
        return MetodoPagoResponse(**created_metodo.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_metodo_pago}", response_model=MetodoPagoResponse)
def update_metodo_pago(id_metodo_pago: int, metodo_data: MetodoPagoUpdate, service: MetodoPagoService = Depends(get_metodo_pago_service)):
    """Actualizar un método de pago existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    metodo_actual = service.get_by_id(id_metodo_pago)
    if not metodo_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Método de pago con ID {id_metodo_pago} no encontrado"
        )
    
    # 2. Merge inteligente
    nueva_descripcion = metodo_data.descripcion if metodo_data.descripcion is not None else metodo_actual.descripcion

    # 3. Crear la instancia para actualizar con los datos mezclados
    metodo_a_guardar = MetodoPago(
        id_metodo_pago=id_metodo_pago,
        descripcion=nueva_descripcion
    )
    
    try:
        service.update(metodo_a_guardar)
        return MetodoPagoResponse(**metodo_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_metodo_pago}", status_code=status.HTTP_204_NO_CONTENT)
def delete_metodo_pago(id_metodo_pago: int, service: MetodoPagoService = Depends(get_metodo_pago_service)):
    """Eliminar un método de pago"""
    existing = service.get_by_id(id_metodo_pago)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Método de pago con ID {id_metodo_pago} no encontrado"
        )
    
    service.delete(id_metodo_pago)
    return None
