# schemas/usuario.py

from pydantic import BaseModel, EmailStr
from typing import Optional

# Esquema base para los datos del usuario
class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr

# Esquema para la creación de un usuario (recibe la contraseña)
class UsuarioCreate(UsuarioBase):
    password: str

# Esquema para devolver un usuario (nunca incluye la contraseña)
class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

# Esquema para actualizar datos del perfil (todos los campos son opcionales)
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None