from __future__ import annotations

import os

from fastapi import FastAPI

if os.environ.get("VERCEL"):
    # Vercel serverless imports the function module before serving any request.
    # The full codex-lb application starts long-running background schedulers and
    # database lifecycle work that is appropriate for a persistent ASGI process,
    # but not for Vercel's per-invocation Python functions. Keep the deployment
    # healthy with lightweight endpoints instead of crashing during import/startup.
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
else:
    from app.main import app

__all__ = ["app"]
