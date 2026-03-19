"""
FastAPI application factory.
Assembles middleware, static files, and all route modules.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import CORS_ORIGINS, APP_TITLE, APP_VERSION, STATIC_DIR, LOG_LEVEL
from app.routes import sorting, graph, health

# --- Logging ---
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# --- App ---
app = FastAPI(title=APP_TITLE, version=APP_VERSION)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(sorting.router)
app.include_router(graph.router)
app.include_router(health.router)


# --- Static file serving ---
@app.get("/")
async def index():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/styles.css")
async def serve_css():
    return FileResponse(str(STATIC_DIR / "styles.css"), media_type="text/css")


@app.get("/script.js")
async def serve_js():
    return FileResponse(str(STATIC_DIR / "script.js"), media_type="application/javascript")


logger.info("App factory initialized — %s v%s", APP_TITLE, APP_VERSION)
