# app/controllers/home_controller.py
"""
Controlador Home
----------------
Funções para upload de arquivos, renderização de páginas, análise de similaridade e dopping.
"""

# Imports FastAPI e SQLAlchemy
from fastapi import UploadFile, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Imports internos do projeto
from app.config.database import SessionLocal, get_db, engine
from app.schemas import schema
from app.models.crud_mol import get_all_molecules
from app.models import crud
from app.utils.match_similarity import match_FP
from app.utils.molecule_designer import render_svg
from app.utils.mass_matrix_builder import frag_matrix_builder, run_anabolic_model
from app.views import templates

# Outros imports
import os
import shutil
from pathlib import Path
import pandas as pd
import plotly.express as px
from plotly.io import to_html

# Inicialização de templates e diretórios
templates = Jinja2Templates(directory="app/views/templates")
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------------- FUNÇÕES DE UPLOAD ----------------------

def handle_file_upload(file: UploadFile):
    """
    Realiza upload de arquivo e salva no diretório de uploads.
    """
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "filename": file.filename,
        "message": "Upload realizado com sucesso!"
    }

# ---------------------- FUNÇÕES DE SIMILARIDADE ----------------------

def get_similarity_page(request: Request, db=None):
    """
    Renderiza página de similaridade.
    """
    # Apenas retorna a página vazia (será preenchida via JS)
    return templates.TemplateResponse("similarity.html", {"request": request, "svg_list": []})

def run_similarity_analysis(
    user_input: str,
    threshold: float,
    mode: str,
    degree_freedom: int = 1
):
    """
    Executa análise de similaridade e gera SVGs.
    """
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
    """
    Renderiza página de busca AAS.
    """
    # Aqui pode ser implementada a lógica necessária para a página de AAS Search
    return templates.TemplateResponse("aas_search.html", {"request": request})


def clean_and_convert(val):
    """
    Limpa e converte valores para float.
    """
    val = val.strip()           # remove espaços
    if val.count('.') > 1:      # se tiver mais de um ponto, corta no segundo
        val = '.'.join(val.split('.')[:2])
    try:
        return float(val)
    except ValueError:
        return None 


def run_dopping_analysis(exact_mass: float, mz_list, intensity_list):
    """
    Executa análise de doping.
    """
    try:
        matrix_ms_fp = frag_matrix_builder(mz_list,intensity_list,exact_mass)
        print(matrix_ms_fp)
        result = run_anabolic_model(matrix_ms_fp)
        if result == 1:
            analise_result = "This sample was classifier as doping"
        else:
            analise_result = "This sample was classifier not doping"
    except Exception as e:
        return f"Erro na dopping: {e}", 500
    return analise_result

def make_plot(mz_list, intensity_list):
    """
    Gera plot da espectrometria de massas.
    """
    # Genarate data
    
    data_plot = {'mz': mz_list, 'intensity': intensity_list}
    df_plot = pd.DataFrame(data_plot)
    
    # Generate plot
    fig = px.bar(df_plot, x='mz', y='intensity', title='Your mass spectra')
    
    # Convert the plot to HTML
    plot_div = to_html(fig, full_html=False, include_plotlyjs='cdn')
    return plot_div
    
    
    

# Função controladora para visualizar os usuários
def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Retorna lista de usuários.
    """
    return crud.get_users(db, skip, limit)