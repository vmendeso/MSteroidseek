# app/routes/auth_routes.py

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models import crud
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.schema import UserCreate, UserRead
import app.controllers.auth_controller as controller

#router = APIRouter(prefix="/usuarios", tags=["Usuários"])

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/", response_class=HTMLResponse)
@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, username)
    if user and user.password == password:
        return RedirectResponse(url="/dashboard", status_code=302)
    return RedirectResponse(url="/login", status_code=302)


@router.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return controller.create_user(user, db)

@router.get(
    "/users",
    response_model=list[UserRead]
)
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return controller.get_all_users(skip, limit, db)

@router.get(
    "/users/{user_id}",
    response_model=UserRead
)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return controller.get_user_by_id(user_id, db)

@router.delete(
    "/users/{user_id}",
    response_model=UserRead
)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return controller.delete_user_by_id(user_id, db)
