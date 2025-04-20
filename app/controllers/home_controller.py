from fastapi import UploadFile
import os
import shutil
from app.config.database import SessionLocal
from app.models import crud
from app.schemas import schema
from sqlalchemy.orm import Session
from app.views import templates
from app.utils.molecule_designer import render_svg
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/views/templates")

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
    smiles_list = ["CCO", "C1=CC=CC=C1", "CC(=O)OC1=CC=CC=C1C(=O)O"]
    svg_list = [render_svg(smiles) for smiles in smiles_list]
    return templates.TemplateResponse("similarity.html", {
        "request": request,
        "svg_list": svg_list
    })
# Função controladora para a página de AAS Search
def get_aas_search_page(request):
    # Aqui pode ser implementada a lógica necessária para a página de AAS Search
    return templates.TemplateResponse("aas_search.html", {"request": request})

# Função controladora para visualizar os usuários
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return crud.get_users(db, skip, limit)