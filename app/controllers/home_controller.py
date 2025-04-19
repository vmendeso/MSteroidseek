from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/views/templates")

def render_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "title": "Minha Página FastAPI MVC"})
