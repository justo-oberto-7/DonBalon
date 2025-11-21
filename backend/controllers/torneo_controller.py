from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.torneo_schema import TorneoCreate, TorneoUpdate, TorneoResponse
from services.torneo_service import TorneoService
from classes.torneo import Torneo
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/torneos", tags=["Torneos"])


def get_torneo_service():
    """Dependency para obtener instancia de TorneoService"""
    db_conn = DatabaseConnection()
    return TorneoService(connection=db_conn.get_connection())


@router.get("/", response_model=List[TorneoResponse])
def list_torneos(service: TorneoService = Depends(get_torneo_service)):
    """Listar todos los torneos"""
    torneos = service.list_all()
    return [TorneoResponse(**torneo.to_dict()) for torneo in torneos]


@router.get("/{id_torneo}", response_model=TorneoResponse)
def get_torneo(id_torneo: int, service: TorneoService = Depends(get_torneo_service)):
    """Obtener un torneo por ID"""
    torneo = service.get_by_id(id_torneo)
    if not torneo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Torneo con ID {id_torneo} no encontrado"
        )
    return TorneoResponse(**torneo.to_dict())


@router.post("/", response_model=TorneoResponse, status_code=status.HTTP_201_CREATED)
def create_torneo(torneo_data: TorneoCreate, service: TorneoService = Depends(get_torneo_service)):
    """Crear un nuevo torneo"""
    # Conversión manual de Schema a Clase de Dominio
    torneo = Torneo(
        nombre=torneo_data.nombre,
        fecha_inicio=torneo_data.fecha_inicio,
        fecha_fin=torneo_data.fecha_fin
    )
    
    try:
        created_torneo = service.insert(torneo)
        return TorneoResponse(**created_torneo.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_torneo}", response_model=TorneoResponse)
def update_torneo(id_torneo: int, torneo_data: TorneoUpdate, service: TorneoService = Depends(get_torneo_service)):
    """Actualizar un torneo existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    torneo_actual = service.get_by_id(id_torneo)
    if not torneo_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Torneo con ID {id_torneo} no encontrado"
        )
    
    # 2. Merge inteligente
    nuevo_nombre = torneo_data.nombre if torneo_data.nombre is not None else torneo_actual.nombre
    nueva_fecha_inicio = torneo_data.fecha_inicio if torneo_data.fecha_inicio is not None else torneo_actual.fecha_inicio
    nueva_fecha_fin = torneo_data.fecha_fin if torneo_data.fecha_fin is not None else torneo_actual.fecha_fin

    # 3. Crear la instancia para actualizar con los datos mezclados
    torneo_a_guardar = Torneo(
        id_torneo=id_torneo,
        nombre=nuevo_nombre,
        fecha_inicio=nueva_fecha_inicio,
        fecha_fin=nueva_fecha_fin
    )
    
    try:
        service.update(torneo_a_guardar)
        return TorneoResponse(**torneo_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_torneo}", status_code=status.HTTP_204_NO_CONTENT)
def delete_torneo(id_torneo: int, service: TorneoService = Depends(get_torneo_service)):
    """Eliminar un torneo"""
    existing = service.get_by_id(id_torneo)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Torneo con ID {id_torneo} no encontrado"
        )
    
    service.delete(id_torneo)
    return None
