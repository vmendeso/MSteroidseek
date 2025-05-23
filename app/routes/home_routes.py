# app/routes/home_routes.py
from fastapi import APIRouter, Request, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
import shutil
from app.config.database import get_db
from app.controllers.home_controller import (
    handle_file_upload,
    get_similarity_page,
    run_similarity_analysis
)
from app.models.mol_model import SimilarityParams  # Parâmetros de similaridade



router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")
UPLOAD_DIR = "uploads"

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/dashboard/similarity", response_class=HTMLResponse)
async def similarity_page(request: Request, db: Session = Depends(get_db)):
    return get_similarity_page(request, db)  # db passado corretamente aqui

@router.post("/run-similarity")
async def run_similarity(request: Request):
    data = await request.json()
    file = data.get("file")
    print(file)
    threshold = data.get("threshold")
    mode = data.get("mode")

    # Lógica de processamento da análise de similaridade
    # Suponha que você obtenha uma lista de SVGs como resultado
    svg_list = run_similarity_analysis(
        user_input=file,
        threshold=threshold,
        mode=mode
    )
    print(svg_list)
    return JSONResponse(content={"svg_list": svg_list, "message": "Análise concluída com sucesso."})

# @router.post("/run-similarity")
# async def run_similarity(params: SimilarityParams):
#     svg_list, message, status = run_similarity_analysis(
#         user_input=params.user_input,
#         threshold=params.threshold,
#         mode=params.mode,
#         degree_freedom=params.degree_freedom
#     )
#     return JSONResponse(content={"svg_list": svg_list, "message": message}, status_code=status)


@router.get("/dashboard/aas-search", response_class=HTMLResponse)
async def aas_page(request: Request):
    return templates.TemplateResponse("aas_search.html", {"request": request})


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    return handle_file_upload(file)