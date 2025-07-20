# app/routes/auth_routes.py

"""
Auth Routes Module
------------------
Este módulo define as rotas de autenticação e gerenciamento de usuários para a aplicação FastAPI.
Inclui rotas para login, criação, consulta e exclusão de usuários.
"""

# Imports de bibliotecas FastAPI e SQLAlchemy
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Imports de módulos internos do projeto
from app.config.database import get_db
from app.models import crud
from app.schemas.schema import UserCreate, UserRead
import app.controllers.auth_controller as controller

# Inicialização do roteador e dos templates Jinja2
router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

# ---------------------- ROTAS DE AUTENTICAÇÃO ----------------------

@router.get("/", response_class=HTMLResponse)
@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    """
    Renderiza a página de login.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Processa o login do usuário. Redireciona para o dashboard se credenciais corretas, senão retorna para login.
    """
    user = crud.get_user_by_username(db, username)
    if user and user.password == password:
        return RedirectResponse(url="/dashboard", status_code=302)
    return RedirectResponse(url="/login", status_code=302)

# ---------------------- ROTAS DE USUÁRIOS ----------------------

@router.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário.
    """
    return controller.create_user(user, db)

@router.get(
    "/users",
    response_model=list[UserRead]
)
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna todos os usuários com paginação.
    """
    return controller.get_all_users(skip, limit, db)

@router.get(
    "/users/{user_id}",
    response_model=UserRead
)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Retorna um usuário pelo ID.
    """
    return controller.get_user_by_id(user_id, db)

@router.delete(
    "/users/{user_id}",
    response_model=UserRead
)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Exclui um usuário pelo ID.
    """
    return controller.delete_user_by_id(user_id, db)
