from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="codex-lb Vercel health")


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok", "service": "codex-lb"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/live")
async def health_live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
async def health_ready() -> dict[str, str]:
    return {"status": "ok"}
