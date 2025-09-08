# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.usuario import Usuario, UsuarioCreate
from services import usuario_service, auth_service
from config.database import get_db
from datetime import timedelta
from config.settings import settings

router = APIRouter()

@router.post("/registrar", response_model=Usuario, status_code=201)
def register_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = usuario_service.get_user_by_email(db, email=user.correo)
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return usuario_service.create_user(db=db, user=user)

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = usuario_service.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": user.correo}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}