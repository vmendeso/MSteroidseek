from fastapi import UploadFile
import os
import shutil
from app.config.database import SessionLocal
from app.models import crud
from app.schemas import schema
from sqlalchemy.orm import Session
from app.views import templates

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def handle_file_upload(file: UploadFile):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "filename": file.filename,
        "message": "Upload realizado com sucesso!"
    }

# Função controladora para a página de Similarity
def get_similarity_page(request):
    # Aqui pode ser implementada a lógica necessária para a página de Similarity
    return templates.TemplateResponse("similarity.html", {"request": request})

# Função controladora para a página de AAS Search
def get_aas_search_page(request):
    # Aqui pode ser implementada a lógica necessária para a página de AAS Search
    return templates.TemplateResponse("aas_search.html", {"request": request})

# Função controladora para visualizar os usuários
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return crud.get_users(db, skip, limit)