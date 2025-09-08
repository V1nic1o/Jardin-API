# models/planta.py

from sqlalchemy import Column, Integer, String, Text
from config.database import Base

class Planta(Base):
    __tablename__ = "plantas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # Ej: "Flor", "Árbol", "Arbusto", etc.
    descripcion = Column(Text, nullable=True)
    imagen_url = Column(String, nullable=True)  # URL del modelo o imagen de referencia
    clima = Column(String, nullable=True)  # Ej: "Tropical", "Templado"
    iluminacion = Column(String, nullable=True)  # Ej: "Sol", "Sombra", "Mixto"