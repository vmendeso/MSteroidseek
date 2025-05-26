from fastapi import UploadFile, Request, Depends
import os
import shutil
from pathlib import Path
import pandas as pd
from app.config.database import SessionLocal, get_db, engine
from app.models.crud_mol import get_all_molecules
from app.utils.match_similarity import match_FP
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

# Função para renderizar a página de similaridade

def get_similarity_page(request: Request, db=None):
    # Apenas retorna a página vazia (será preenchida via JS)
    return templates.TemplateResponse("similarity.html", {"request": request, "svg_list": []})

# Função de análise de similaridade que lê o banco completo, extrai m/z e depois gera SVGs

def run_similarity_analysis(
    user_input: str,
    threshold: float,
    mode: str,
    degree_freedom: int = 1
):
    try:
        df_full = pd.read_sql_table(
            table_name="similary_structur_mol",
            con=engine,
            schema="msteroid"
        )
        df_fpx = pd.read_csv("app/config/data/df_fp1_all_EI.csv")
        df_fpx = df_fpx.drop(df_fpx.columns[0], axis=1)
    except Exception as e:
        return [], f"Erro ao ler tabela do banco: {e}", 500

    if "m/z" not in df_full.columns:
        return [], "Coluna 'm/z' não encontrada na tabela.", 400
    
    with open(f'uploads/{user_input}', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    print(conteudo)
    user_input = conteudo
    #user_input= '59, 130, 131, 131, 131, 132, 133, 147, 148, 149, 149, 151, 161, 163, 177, 193, 237, 251, 267, 382'
    try:
        result_dict = match_FP(
            user_input=user_input,
            degree_freedom=degree_freedom,
            df_fpx=df_fpx,
            df_db=df_full,
            threshold=threshold,
            metric=mode
        )
    except Exception as e:
        return [], f"Erro na similaridade: {e}", 500

    svg_list = []
    for idx_str in result_dict.keys():
        try:
            idx = int(idx_str)
            smiles = df_full.at[idx, "smiles"]
            svg_list.append(render_svg(smiles))
        except Exception:
            continue

    message = "Análise concluída com sucesso!"
    return svg_list


# Função controladora para a página de AAS Search
def get_aas_search_page(request):
    # Aqui pode ser implementada a lógica necessária para a página de AAS Search
    return templates.TemplateResponse("aas_search.html", {"request": request})

def run_dopping_analysis(user_input: str):
    with open(f'uploads/{user_input}', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    print(conteudo)
    user_input = conteudo
    

# Função controladora para visualizar os usuários
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return crud.get_users(db, skip, limit)