# services/usuario_service.py
from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate
from passlib.context import CryptContext
from services import auth_service 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.correo == email).first()

def create_user(db: Session, user: UsuarioCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = Usuario(
        correo=user.correo,
        nombre=user.nombre,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not auth_service.verify_password(password, user.hashed_password):
        return False
    return user