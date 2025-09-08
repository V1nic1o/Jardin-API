# services/diseno_service.py

from sqlalchemy.orm import Session
from models.diseno import Diseno
from schemas.diseno import DisenoCreate
import json

# Crear diseño
def crear_diseno(db: Session, diseno_data: DisenoCreate, usuario_id: int):
    # Serializar la lista de plantas usadas a texto JSON
    plantas_json = json.dumps([planta.dict() for planta in diseno_data.plantas_usadas])

    nuevo_diseno = Diseno(
        nombre=diseno_data.nombre,
        descripcion=diseno_data.descripcion,
        imagen_url=diseno_data.imagen_url,
        usuario_id=usuario_id,
        plantas_usadas=plantas_json
    )
    db.add(nuevo_diseno)
    db.commit()
    db.refresh(nuevo_diseno)
    return nuevo_diseno

# Obtener todos los diseños del usuario
def obtener_disenos_por_usuario(db: Session, usuario_id: int):
    return db.query(Diseno).filter(Diseno.usuario_id == usuario_id).all()

# Obtener diseño por ID (solo si pertenece al usuario)
def obtener_diseno_por_id(db: Session, diseno_id: int, usuario_id: int):
    return db.query(Diseno).filter(Diseno.id == diseno_id, Diseno.usuario_id == usuario_id).first()

# Actualizar diseño
def actualizar_diseno(db: Session, diseno_id: int, diseno_data: DisenoCreate, usuario_id: int):
    diseno = obtener_diseno_por_id(db, diseno_id, usuario_id)
    if not diseno:
        return None

    diseno.nombre = diseno_data.nombre
    diseno.descripcion = diseno_data.descripcion
    diseno.imagen_url = diseno_data.imagen_url
    diseno.plantas_usadas = json.dumps([planta.dict() for planta in diseno_data.plantas_usadas])

    db.commit()
    db.refresh(diseno)
    return diseno

# Eliminar diseño
def eliminar_diseno(db: Session, diseno_id: int, usuario_id: int):
    diseno = obtener_diseno_por_id(db, diseno_id, usuario_id)
    if diseno:
        db.delete(diseno)
        db.commit()
    return diseno