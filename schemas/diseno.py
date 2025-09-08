# schemas/diseno.py

from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

# Estructura interna para cada planta usada
class PlantaUsada(BaseModel):
    planta_id: int
    nombre: str
    cantidad: int

# Base del diseño (usado en entrada y salida)
class DisenoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    plantas_usadas: List[PlantaUsada]
    imagen_url: Optional[HttpUrl] = None  # Puede ser null por ahora

# Esquema de creación de diseño
class DisenoCreate(DisenoBase):
    pass

# Esquema de salida al frontend
class Diseno(DisenoBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True