# routes/diseno.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import StreamingResponse

from schemas.diseno import Diseno, DisenoCreate, PlantaUsada
from services import diseno_service
from config.database import get_db
from utils.auth_utils import get_current_user
from models.usuario import Usuario
from utils.cloudinary_uploader import subir_imagen_a_cloudinary
from utils.pdf_generator import generar_pdf_diseno
import json

router = APIRouter()

# Crear diseño con imagen (protegido)
@router.post("/", response_model=Diseno, status_code=status.HTTP_201_CREATED)
def crear_diseno(
    nombre: str = Form(...),
    descripcion: str = Form(None),
    plantas_usadas: str = Form(...),  # JSON como string
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        imagen_url = subir_imagen_a_cloudinary(file.file) if file else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir imagen: {str(e)}")

    # Convertir string a lista de objetos PlantaUsada
    try:
        plantas_dict = json.loads(plantas_usadas)
        plantas = [PlantaUsada(**planta) for planta in plantas_dict]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar plantas_usadas: {str(e)}")

    diseno_data = DisenoCreate(
        nombre=nombre,
        descripcion=descripcion,
        imagen_url=imagen_url,
        plantas_usadas=plantas
    )

    return diseno_service.crear_diseno(db, diseno_data, current_user.id)

# Obtener todos los diseños del usuario (protegido)
@router.get("/", response_model=List[Diseno])
def obtener_mis_disenos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return diseno_service.obtener_disenos_por_usuario(db, current_user.id)

# Obtener diseño específico por ID (protegido)
@router.get("/{diseno_id}", response_model=Diseno)
def obtener_diseno(
    diseno_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    diseno = diseno_service.obtener_diseno_por_id(db, diseno_id, current_user.id)
    if not diseno:
        raise HTTPException(status_code=404, detail="Diseño no encontrado")
    return diseno

# Actualizar diseño (protegido)
@router.put("/{diseno_id}", response_model=Diseno)
def actualizar_diseno(
    diseno_id: int,
    diseno_actualizado: DisenoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    diseno = diseno_service.actualizar_diseno(db, diseno_id, diseno_actualizado, current_user.id)
    if not diseno:
        raise HTTPException(status_code=404, detail="Diseño no encontrado")
    return diseno

# Eliminar diseño (protegido)
@router.delete("/{diseno_id}", response_model=Diseno)
def eliminar_diseno(
    diseno_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    diseno = diseno_service.eliminar_diseno(db, diseno_id, current_user.id)
    if not diseno:
        raise HTTPException(status_code=404, detail="Diseño no encontrado")
    return diseno

# Generar PDF del diseño (protegido)
@router.get("/{diseno_id}/pdf", response_class=StreamingResponse)
def generar_pdf(
    diseno_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    diseno = diseno_service.obtener_diseno_por_id(db, diseno_id, current_user.id)
    if not diseno:
        raise HTTPException(status_code=404, detail="Diseño no encontrado")

    # Convertir JSON string a lista de dicts
    try:
        plantas = json.loads(diseno.plantas_usadas)
    except Exception:
        plantas = []

    diseno_dict = {
        "nombre": diseno.nombre,
        "fecha_creacion": diseno.fecha_creacion,
        "imagen_url": diseno.imagen_url,
        "plantas_usadas": plantas
    }

    pdf_buffer = generar_pdf_diseno(diseno_dict, current_user.nombre)

    return StreamingResponse(
        content=pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=diseno_{diseno.id}.pdf"}
    )