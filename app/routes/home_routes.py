# app/routes/home_routes.py
from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
import shutil
from app.config.database import get_db
from app.controllers.home_controller import (
    handle_file_upload,
    get_similarity_page,
    run_similarity_analysis,
    run_dopping_analysis
)
from app.models.mol_model import SimilarityParams, DoppingRequest # Parâmetros de similaridade
import pandas as pd


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

@router.post("/run-dopping")
async def run_dopping(payload: DoppingRequest):
    mz_path = os.path.join(UPLOAD_DIR, payload.mz_file)
    intensity_path = os.path.join(UPLOAD_DIR, payload.intensity_file)
    exact_mass = payload.exact_mass

    if not os.path.exists(mz_path) or not os.path.exists(intensity_path):
        raise HTTPException(status_code=404, detail="Arquivos não encontrados.")
    
    # Parametros e dados dopping
    mz_user = list(pd.read_csv(mz_path))
    with open(intensity_path, 'r', encoding='utf-8') as f:
        intensity_user = f.read()
    #intensity_user = list(intensity_user)
    intensity_user = [v for v in intensity_user.split(',')]
    
    # Simulação do processamento
    try:
        result_dopping = run_dopping_analysis(exact_mass, mz_user, intensity_user)
        print(f"Rodando análise para o composto: {exact_mass}")
        print(f"Usando arquivos: {mz_user}, {intensity_user}")
        print(f"Result analise: {result_dopping}")

       
        return JSONResponse(content={
                            "message": f"Análise realizada com sucesso para {exact_mass}.",
                            "result": result_dopping  
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar análise: {str(e)}")

@router.get("/dashboard/aas-search", response_class=HTMLResponse)
async def aas_page(request: Request):
    return templates.TemplateResponse("aas_search.html", {"request": request})


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    return handle_file_upload(file)