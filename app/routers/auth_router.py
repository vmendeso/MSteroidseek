from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from app.controllers.auth_controller import show_login_form, process_login

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return show_login_form(request)

@router.post("/login", response_class=HTMLResponse)
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    return process_login(request, username, password)