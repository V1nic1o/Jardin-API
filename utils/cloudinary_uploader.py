# utils/cloudinary_uploader.py

import cloudinary
import cloudinary.uploader
from config.settings import settings

# Configurar conexión con Cloudinary
cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)

def subir_imagen_a_cloudinary(file):
    result = cloudinary.uploader.upload(file)
    return result.get("secure_url")