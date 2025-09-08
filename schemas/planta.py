# schemas/planta.py

from pydantic import BaseModel
from typing import Optional

class PlantaBase(BaseModel):
    nombre: str
    tipo: str
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    clima: Optional[str] = None
    iluminacion: Optional[str] = None

class PlantaCreate(PlantaBase):
    pass  # Es igual que PlantaBase, pero puedes extenderlo en el futuro

class Planta(PlantaBase):
    id: int

    class Config:
        from_attributes = True