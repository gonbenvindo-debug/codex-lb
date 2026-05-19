## ADDED Requirements

### Requirement: Vercel deployment uses static SPA plus a single Python backend

The Vercel deployment SHALL expose the dashboard SPA as static assets from `public/` and SHALL route backend traffic through one FastAPI Python Function entrypoint. The deployment MUST NOT expose Python source files as public content.

#### Scenario: SPA traffic stays on static hosting

- **WHEN** a browser requests `/`, a deep dashboard route, or frontend asset paths such as `/assets/*`
- **THEN** Vercel serves static content from the built `public/` directory
- **AND** the request does not require the Python runtime

#### Scenario: Backend paths invoke the Python function

- **WHEN** a client requests `/api/*`, `/v1/*`, `/backend-api/*`, `/health*`, or protected internal maintenance routes
- **THEN** Vercel routes the request to the FastAPI Python Function
- **AND** the FastAPI app handles the original request path

#### Scenario: Python source is never served as static content

- **WHEN** the project is deployed to Vercel
- **THEN** the root URL does not return the contents of `index.py`, `api/index.py`, or any other Python source file

### Requirement: Vercel runtime uses serverless-safe maintenance flow

When `codex-lb` runs in Vercel serverless mode, it MUST avoid persistent per-instance maintenance loops and MUST instead expose protected one-shot maintenance endpoints for Cron Jobs.

#### Scenario: Serverless mode disables long-lived background loops

- **WHEN** the application starts with serverless mode enabled
- **THEN** usage refresh, model refresh, sticky-session cleanup, API-key reset loops, cache invalidation polling, bridge registration, and metrics listeners do not start as background tasks

#### Scenario: Cron endpoints run maintenance safely

- **WHEN** a protected internal cron endpoint is invoked with the configured cron bearer secret
- **THEN** the application runs the corresponding maintenance task once
- **AND** it returns a successful health-style response when the task completes without error
