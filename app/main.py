# app/main.py
"""
Módulo principal da aplicação FastAPI
-------------------------------------
Inicializa a aplicação, configura diretórios, carrega dados e inclui rotas principais.
"""

# Imports de bibliotecas FastAPI e SQLAlchemy
from fastapi import FastAPI
from sqlalchemy import text
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Imports internos do projeto
from app.config.database import engine, Base, load_dataframe_to_db
from app.routes import auth_routes, home_routes
import os

# ---------------------- BANCO DE DADOS ----------------------
# Criação do schema no banco de dados
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS msteroid"))

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# Carregando dados no database
load_dataframe_to_db()

# ---------------------- INICIALIZAÇÃO DA APP ----------------------
app = FastAPI(title="User API")

# Diretórios estáticos
app.mount("/static", StaticFiles(directory="app/views/static"), name="static")
templates = Jinja2Templates(directory="app/views/templates")

# Pasta de uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------------- INCLUSÃO DE ROTAS ----------------------
app.include_router(auth_routes.router)
app.include_router(home_routes.router)

# ...fim do arquivo...
