from fastapi import FastAPI
from app.routers import coldemail
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR.parent / "templates"
STATIC_DIR = BASE_DIR.parent / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

app.include_router(coldemail.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    """Serve the main HTML page"""
    return templates.TemplateResponse("index.html", {"request": request})