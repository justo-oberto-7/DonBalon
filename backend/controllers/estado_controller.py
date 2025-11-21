from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.estado_schema import EstadoCreate, EstadoUpdate, EstadoResponse
from services.estado_service import EstadoService
from classes.estado import Estado
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/estados", tags=["Estados"])


def get_estado_service():
    """Dependency para obtener instancia de EstadoService"""
    db_conn = DatabaseConnection()
    return EstadoService(connection=db_conn.get_connection())


@router.get("/", response_model=List[EstadoResponse])
def list_estados(service: EstadoService = Depends(get_estado_service)):
    """Listar todos los estados"""
    estados = service.list_all()
    return [EstadoResponse(**estado.to_dict()) for estado in estados]


@router.get("/{id_estado}", response_model=EstadoResponse)
def get_estado(id_estado: int, service: EstadoService = Depends(get_estado_service)):
    """Obtener un estado por ID"""
    estado = service.get_by_id(id_estado)
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estado con ID {id_estado} no encontrado"
        )
    return EstadoResponse(**estado.to_dict())


@router.post("/", response_model=EstadoResponse, status_code=status.HTTP_201_CREATED)
def create_estado(estado_data: EstadoCreate, service: EstadoService = Depends(get_estado_service)):
    """Crear un nuevo estado"""
    # Conversión manual de Schema a Clase de Dominio
    estado = Estado(
        nombre=estado_data.nombre,
        ambito=estado_data.ambito
    )
    
    try:
        created_estado = service.insert(estado)
        return EstadoResponse(**created_estado.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_estado}", response_model=EstadoResponse)
def update_estado(id_estado: int, estado_data: EstadoUpdate, service: EstadoService = Depends(get_estado_service)):
    """Actualizar un estado existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    estado_actual = service.get_by_id(id_estado)
    if not estado_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estado con ID {id_estado} no encontrado"
        )
    
    # 2. Merge inteligente
    nuevo_nombre = estado_data.nombre if estado_data.nombre is not None else estado_actual.nombre
    nuevo_ambito = estado_data.ambito if estado_data.ambito is not None else estado_actual.ambito

    # 3. Crear la instancia para actualizar con los datos mezclados
    estado_a_guardar = Estado(
        id_estado=id_estado,
        nombre=nuevo_nombre,
        ambito=nuevo_ambito
    )
    
    try:
        service.update(estado_a_guardar)
        return EstadoResponse(**estado_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_estado}", status_code=status.HTTP_204_NO_CONTENT)
def delete_estado(id_estado: int, service: EstadoService = Depends(get_estado_service)):
    """Eliminar un estado"""
    existing = service.get_by_id(id_estado)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estado con ID {id_estado} no encontrado"
        )
    
    service.delete(id_estado)
    return None
