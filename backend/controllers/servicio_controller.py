from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.servicio_schema import ServicioCreate, ServicioUpdate, ServicioResponse
from services.servicio_service import ServicioService
from classes.servicio import Servicio
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/servicios", tags=["Servicios"])


def get_servicio_service():
    """Dependency para obtener instancia de ServicioService"""
    db_conn = DatabaseConnection()
    return ServicioService(connection=db_conn.get_connection())


@router.get("/", response_model=List[ServicioResponse])
def list_servicios(service: ServicioService = Depends(get_servicio_service)):
    """Listar todos los servicios"""
    servicios = service.list_all()
    return [ServicioResponse(**servicio.to_dict()) for servicio in servicios]


@router.get("/{id_servicio}", response_model=ServicioResponse)
def get_servicio(id_servicio: int, service: ServicioService = Depends(get_servicio_service)):
    """Obtener un servicio por ID"""
    servicio = service.get_by_id(id_servicio)
    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {id_servicio} no encontrado"
        )
    return ServicioResponse(**servicio.to_dict())


@router.post("/", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def create_servicio(servicio_data: ServicioCreate, service: ServicioService = Depends(get_servicio_service)):
    """Crear un nuevo servicio"""
    # Conversión manual de Schema a Clase de Dominio
    servicio = Servicio(
        descripcion=servicio_data.descripcion,
        costo_servicio=servicio_data.costo_servicio
    )
    
    try:
        created_servicio = service.insert(servicio)
        return ServicioResponse(**created_servicio.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_servicio}", response_model=ServicioResponse)
def update_servicio(id_servicio: int, servicio_data: ServicioUpdate, service: ServicioService = Depends(get_servicio_service)):
    """Actualizar un servicio existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    servicio_actual = service.get_by_id(id_servicio)
    if not servicio_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {id_servicio} no encontrado"
        )
    
    # 2. Merge inteligente
    nueva_descripcion = servicio_data.descripcion if servicio_data.descripcion is not None else servicio_actual.descripcion
    nuevo_costo = servicio_data.costo_servicio if servicio_data.costo_servicio is not None else servicio_actual.costo_servicio

    # 3. Crear la instancia para actualizar con los datos mezclados
    servicio_a_guardar = Servicio(
        id_servicio=id_servicio,
        descripcion=nueva_descripcion,
        costo_servicio=nuevo_costo
    )
    
    try:
        service.update(servicio_a_guardar)
        return ServicioResponse(**servicio_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_servicio}", status_code=status.HTTP_204_NO_CONTENT)
def delete_servicio(id_servicio: int, service: ServicioService = Depends(get_servicio_service)):
    """Eliminar un servicio"""
    existing = service.get_by_id(id_servicio)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {id_servicio} no encontrado"
        )
    
    service.delete(id_servicio)
    return None
