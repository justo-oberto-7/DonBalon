from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.equipo_schema import EquipoCreate, EquipoUpdate, EquipoResponse
from services.equipo_service import EquipoService
from classes.equipo import Equipo
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/equipos", tags=["Equipos"])


def get_equipo_service():
    """Dependency para obtener instancia de EquipoService"""
    db_conn = DatabaseConnection()
    return EquipoService(connection=db_conn.get_connection())


@router.get("/", response_model=List[EquipoResponse])
def list_equipos(service: EquipoService = Depends(get_equipo_service)):
    """Listar todos los equipos"""
    equipos = service.list_all()
    return [EquipoResponse(**equipo.to_dict()) for equipo in equipos]


@router.get("/{id_equipo}", response_model=EquipoResponse)
def get_equipo(id_equipo: int, service: EquipoService = Depends(get_equipo_service)):
    """Obtener un equipo por ID"""
    equipo = service.get_by_id(id_equipo)
    if not equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo con ID {id_equipo} no encontrado"
        )
    return EquipoResponse(**equipo.to_dict())


@router.post("/", response_model=EquipoResponse, status_code=status.HTTP_201_CREATED)
def create_equipo(equipo_data: EquipoCreate, service: EquipoService = Depends(get_equipo_service)):
    """Crear un nuevo equipo"""
    # Conversión manual de Schema a Clase de Dominio
    equipo = Equipo(
        id_torneo=equipo_data.id_torneo,
        nombre=equipo_data.nombre,
        cant_jugadores=equipo_data.cant_jugadores
    )
    
    try:
        created_equipo = service.insert(equipo)
        return EquipoResponse(**created_equipo.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_equipo}", response_model=EquipoResponse)
def update_equipo(id_equipo: int, equipo_data: EquipoUpdate, service: EquipoService = Depends(get_equipo_service)):
    """Actualizar un equipo existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    equipo_actual = service.get_by_id(id_equipo)
    if not equipo_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo con ID {id_equipo} no encontrado"
        )
    
    # 2. Merge inteligente
    nuevo_torneo = equipo_data.id_torneo if equipo_data.id_torneo is not None else equipo_actual.id_torneo
    nuevo_nombre = equipo_data.nombre if equipo_data.nombre is not None else equipo_actual.nombre
    nueva_cant = equipo_data.cant_jugadores if equipo_data.cant_jugadores is not None else equipo_actual.cant_jugadores

    # 3. Crear la instancia para actualizar con los datos mezclados
    equipo_a_guardar = Equipo(
        id_equipo=id_equipo,
        id_torneo=nuevo_torneo,
        nombre=nuevo_nombre,
        cant_jugadores=nueva_cant
    )
    
    try:
        service.update(equipo_a_guardar)
        return EquipoResponse(**equipo_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_equipo}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipo(id_equipo: int, service: EquipoService = Depends(get_equipo_service)):
    """Eliminar un equipo"""
    existing = service.get_by_id(id_equipo)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo con ID {id_equipo} no encontrado"
        )
    
    service.delete(id_equipo)
    return None
