# app/routes/home_routes.py
from fastapi import APIRouter, Request, Depends, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
import shutil
from app.controllers.home_controller import handle_file_upload, get_similarity_page

from app.config.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")
UPLOAD_DIR = "uploads"

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/dashboard/similarity")
async def similarity_page(request: Request):
    return get_similarity_page(request)


@router.get("/dashboard/aas-search", response_class=HTMLResponse)
async def aas_page(request: Request):
    return templates.TemplateResponse("aas_search.html", {"request": request})


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    return handle_file_upload(file)