# utils/pdf_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

def generar_pdf_diseno(diseno: dict, usuario_nombre: str):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Título
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 50, f"Resumen de Diseño: {diseno['nombre']}")

    # Usuario y fecha
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 80, f"Usuario: {usuario_nombre}")
    pdf.drawString(50, height - 100, f"Fecha de creación: {diseno['fecha_creacion'].strftime('%Y-%m-%d %H:%M')}")

    # Imagen (opcional)
    if diseno['imagen_url']:
        try:
            from reportlab.platypus import Image
            from urllib.request import urlopen
            img_data = urlopen(diseno['imagen_url']).read()
            img = Image(BytesIO(img_data))
            img.drawHeight = 120
            img.drawWidth = 180
            pdf.drawImage(BytesIO(img_data), 50, height - 280, width=180, height=120)
        except Exception:
            pdf.drawString(50, height - 280, "[No se pudo cargar la imagen]")

    # Tabla de plantas
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 320, "Plantas utilizadas:")

    y = height - 340
    pdf.setFont("Helvetica", 12)
    for planta in diseno['plantas_usadas']:
        pdf.drawString(60, y, f"- {planta['nombre']} (Cantidad: {planta['cantidad']})")
        y -= 20

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer