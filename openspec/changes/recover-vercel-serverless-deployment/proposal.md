## Why

The current Vercel deployment no longer invokes the FastAPI backend. The latest production deployment serves Python source as static content at the root URL, `/health` returns `404`, and the dashboard SPA is not being emitted as CDN-served assets. This breaks the core `codex-lb` surface and wastes Fast Origin Transfer by routing frontend traffic through the wrong layer.

## What Changes

- Rebuild the Vercel integration around a single FastAPI Python Function entrypoint plus static SPA assets in `public/`
- Add a Vercel build script that installs and builds the frontend into `public/` without changing Docker/local `app/static` behavior
- Replace the current rewrites with an API-first routing table that sends `/api/*`, `/v1/*`, `/backend-api/*`, `/health*`, and internal maintenance paths to the Python Function while keeping all other routes on the SPA
- Introduce an explicit serverless mode that trims DB pools, forces HTTP/SSE-compatible upstream transport, and disables long-lived background loops inside Vercel Functions
- Add protected internal cron endpoints so periodic usage refresh, model refresh, sticky cleanup, and API-key reset work via Vercel Cron Jobs instead of per-instance background tasks

## Impact

- Affected specs: `frontend-architecture`, `deployment-installation`
- Affected code:
  - `api/index.py`
  - `app/main.py`
  - `app/core/config/settings.py`
  - `app/modules/health/api.py`
  - scheduler modules under `app/core` and `app/modules`
  - `frontend/vite.config.ts`
  - `vercel.json`
  - `pyproject.toml`
