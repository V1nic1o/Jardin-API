# routes/perfil.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.usuario import UsuarioUpdate, Usuario as UsuarioSchema
from config.database import get_db
from utils.auth_utils import get_current_user
from models.usuario import Usuario
from services import auth_service
from typing import Optional

router = APIRouter()


@router.get("/", response_model=UsuarioSchema)
def obtener_perfil(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return current_user


@router.put("/", response_model=UsuarioSchema)
def actualizar_perfil(
    datos_actualizados: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Verificar si el correo ya existe (y no es el mismo usuario)
    if datos_actualizados.correo and datos_actualizados.correo != current_user.correo:
        usuario_existente = db.query(Usuario).filter(Usuario.correo == datos_actualizados.correo).first()
        if usuario_existente:
            raise HTTPException(status_code=400, detail="El correo ya está en uso por otro usuario")

    # Actualizar campos opcionales
    if datos_actualizados.nombre:
        current_user.nombre = datos_actualizados.nombre
    if datos_actualizados.correo:
        current_user.correo = datos_actualizados.correo
    if datos_actualizados.password:
        current_user.hashed_password = auth_service.get_password_hash(datos_actualizados.password)

    db.commit()
    db.refresh(current_user)
    return current_user