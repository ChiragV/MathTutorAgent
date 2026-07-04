from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from orchestrator import process_request

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="Math Tutor UI")


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    html_path = ROOT / "ui" / "templates" / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.post("/api/generate")
async def generate(payload: dict[str, Any]) -> JSONResponse:
    result = process_request(payload)
    return JSONResponse(result)
