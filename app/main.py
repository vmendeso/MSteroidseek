from fastapi import FastAPI
from sqlalchemy import text
from app.config.database import engine
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS msteroid"))
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config.database import Base, engine, load_dataframe_to_db
from app.routes import auth_routes, home_routes
import os


# Criação das tabelas
Base.metadata.create_all(bind=engine)

# carregando dados no database
load_dataframe_to_db()

# Inicialização da aplicação
app = FastAPI(title="User API")

# Diretórios estáticos
app.mount("/static", StaticFiles(directory="app/views/static"), name="static")
templates = Jinja2Templates(directory="app/views/templates")

# Pasta de uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Inclusão de rotas
app.include_router(auth_routes.router)
app.include_router(home_routes.router)
