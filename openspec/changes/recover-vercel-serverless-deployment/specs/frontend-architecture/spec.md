## MODIFIED Requirements

### Requirement: Vite project structure

The frontend SHALL remain a standalone Vite + React + TypeScript project located at `frontend/` in the repository root. The default production build output SHALL target `app/static/` for local and containerized deployments, and the Vercel build flow SHALL be able to emit the same built assets to `public/` so the platform serves them directly from its static layer.

#### Scenario: Default production build

- **WHEN** a developer runs the standard frontend production build locally
- **THEN** Vite outputs optimized assets (JS, CSS, `index.html`) to `app/static/`

#### Scenario: Vercel production build

- **WHEN** the Vercel build pipeline runs the repository build script
- **THEN** the frontend dependencies are installed
- **AND** Vite emits optimized assets to `public/`
- **AND** the resulting deployment serves the SPA and asset files from Vercel static hosting instead of the Python runtime
