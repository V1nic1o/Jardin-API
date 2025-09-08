# models/diseno.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class Diseno(Base):
    __tablename__ = "disenos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    imagen_url = Column(String, nullable=True)  # Captura del jardín (opcional por ahora)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relación con usuario
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", backref="disenos")

    # Lista de plantas usadas como texto (json simplificado por ahora)
    plantas_usadas = Column(Text, nullable=False)