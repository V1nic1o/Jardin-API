# routes/planta.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schemas.planta import Planta, PlantaCreate
from services import planta_service
from config.database import get_db

# Protección JWT
from utils.auth_utils import get_current_user
from models.usuario import Usuario

router = APIRouter()

# Obtener todas las plantas (público)
@router.get("/", response_model=List[Planta])
def listar_plantas(db: Session = Depends(get_db)):
    return planta_service.obtener_plantas(db)

# Crear nueva planta (requiere autenticación)
@router.post("/", response_model=Planta, status_code=status.HTTP_201_CREATED)
def crear_planta(
    planta: PlantaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return planta_service.crear_planta(db, planta)

# Obtener planta por ID (público)
@router.get("/{planta_id}", response_model=Planta)
def obtener_planta(planta_id: int, db: Session = Depends(get_db)):
    planta = planta_service.obtener_planta_por_id(db, planta_id)
    if not planta:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    return planta

# Actualizar planta (requiere autenticación)
@router.put("/{planta_id}", response_model=Planta)
def actualizar_planta(
    planta_id: int,
    planta_actualizada: PlantaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    planta = planta_service.actualizar_planta(db, planta_id, planta_actualizada)
    if not planta:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    return planta

# Eliminar planta (requiere autenticación)
@router.delete("/{planta_id}", response_model=Planta)
def eliminar_planta(
    planta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    planta = planta_service.eliminar_planta(db, planta_id)
    if not planta:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    return planta