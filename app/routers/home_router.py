from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.controllers.home_controller import render_home

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render_home(request)