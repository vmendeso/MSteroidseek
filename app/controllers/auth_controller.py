from fastapi import Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.user_model import User
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/views/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

def process_login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    
    if user and user.password == password:
        response = RedirectResponse(url="/", status_code=302)
        return response
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "message": "Usuário ou senha inválidos!"
        })