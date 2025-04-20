from fastapi import FastAPI, Depends, HTTPException, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from app.models import crud
from fastapi.templating import Jinja2Templates
from app.config.database import SessionLocal, engine, Base
import os
import shutil

from app.models.schemas import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User API")
app.mount("/static", StaticFiles(directory="app/views/static"), name="static")
templates = Jinja2Templates(directory="app/views/templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    from app.models import crud
    user = crud.get_user_by_username(db, username)
    if user and user.password == password:
        return RedirectResponse(url="/dashboard", status_code=302)
    return RedirectResponse(url="/login", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/dashboard/similarity", response_class=HTMLResponse)
async def similarity_page(request: Request):
    return templates.TemplateResponse("similarity.html", {"request": request})

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "Upload realizado com sucesso!"}

@app.get("/dashboard/aas-search", response_class=HTMLResponse)
async def aas_page(request: Request):
    return templates.TemplateResponse("aas_search.html", {"request": request})

@app.post("/users/", response_model=schemas.UserRead)
def create(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.UserRead)
def read(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@app.get("/users/", response_model=list[schemas.UserRead])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)

@app.delete("/users/{user_id}", response_model=schemas.UserRead)
def delete(user_id: int, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return deleted_user