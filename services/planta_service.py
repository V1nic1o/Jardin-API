# services/planta_service.py

from sqlalchemy.orm import Session
from models.planta import Planta
from schemas.planta import PlantaCreate

# Crear nueva planta
def crear_planta(db: Session, planta: PlantaCreate):
    nueva_planta = Planta(**planta.dict())
    db.add(nueva_planta)
    db.commit()
    db.refresh(nueva_planta)
    return nueva_planta

# Obtener todas las plantas
def obtener_plantas(db: Session):
    return db.query(Planta).all()

# Obtener planta por ID
def obtener_planta_por_id(db: Session, planta_id: int):
    return db.query(Planta).filter(Planta.id == planta_id).first()

# Actualizar planta
def actualizar_planta(db: Session, planta_id: int, planta_actualizada: PlantaCreate):
    planta = obtener_planta_por_id(db, planta_id)
    if planta:
        for key, value in planta_actualizada.dict().items():
            setattr(planta, key, value)
        db.commit()
        db.refresh(planta)
    return planta

# Eliminar planta
def eliminar_planta(db: Session, planta_id: int):
    planta = obtener_planta_por_id(db, planta_id)
    if planta:
        db.delete(planta)
        db.commit()
    return planta