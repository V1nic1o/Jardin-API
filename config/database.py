# config/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Importa la configuración desde settings.py
from .settings import settings

# ¡Línea clave! Usa la URL de la configuración en lugar de tenerla aquí
DATABASE_URL = settings.database_url 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# La dependencia no cambia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()