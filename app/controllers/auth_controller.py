# app/controllers/auth_controller.py
"""
Controlador de Autenticação
--------------------------
Funções para autenticação, criação, consulta e exclusão de usuários.
"""

# Imports FastAPI e SQLAlchemy
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

# Imports internos do projeto
from app.config.database import get_db
from app.models import crud
from app.schemas import schema

# ---------------------- FUNÇÕES DE AUTENTICAÇÃO ----------------------

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    """
    Autentica usuário pelo nome e senha.
    """
    user = crud.get_user_by_username(db, username)
    if user and user.password == password:
        return user
    return None

# ---------------------- FUNÇÕES DE USUÁRIO ----------------------

def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário se não existir.
    """
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return crud.create_user(db, user)

def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Retorna usuário pelo ID.
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna todos os usuários com paginação.
    """
    return crud.get_users(db, skip, limit)

def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Exclui usuário pelo ID.
    """
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
