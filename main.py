# main.py
from fastapi import FastAPI
from models.usuario import Base
from config.database import engine
from routes import auth
from routes import planta
from routes import diseno
from routes import perfil

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JardínAR API",
    description="API para la aplicación de diseño de jardines en Realidad Aumentada.",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(planta.router, prefix="/plantas", tags=["Plantas"])
app.include_router(diseno.router, prefix="/disenos", tags=["Diseños de Jardín"])
app.include_router(perfil.router, prefix="/perfil", tags=["Perfil"])

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de JardínAR!"}