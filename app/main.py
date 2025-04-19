from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.models import schemas, crud
from fastapi.templating import Jinja2Templates
from app.config.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User API")
templates = Jinja2Templates(directory="app/views/templates")

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