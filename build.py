from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = REPO_ROOT / "frontend"
PUBLIC_DIR = REPO_ROOT / "public"


def _run(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    print(f"[build.py] running: {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def _frontend_package_managers() -> list[tuple[list[str], list[str], str]]:
    package_json = json.loads((FRONTEND_DIR / "package.json").read_text(encoding="utf-8"))
    package_manager = str(package_json.get("packageManager", ""))
    candidates: list[tuple[list[str], list[str], str]] = []

    if shutil.which("bun"):
        candidates.append((["bun", "install", "--frozen-lockfile"], ["bun", "run", "build"], "bun"))
    if package_manager.startswith("bun@") and shutil.which("corepack"):
        candidates.append(
            (
                ["corepack", "bun", "install", "--frozen-lockfile"],
                ["corepack", "bun", "run", "build"],
                "corepack bun",
            )
        )
    if shutil.which("npm"):
        candidates.append((["npm", "install", "--no-audit", "--no-fund"], ["npm", "run", "build"], "npm"))
    if not candidates:
        raise RuntimeError("No supported frontend package manager found. Install bun, corepack, or npm.")
    return candidates


def main() -> int:
    env = os.environ.copy()
    env["CODEX_LB_FRONTEND_OUT_DIR"] = "../public"
    PUBLIC_DIR.mkdir(exist_ok=True)
    last_error: subprocess.CalledProcessError | None = None

    for install_command, build_command, label in _frontend_package_managers():
        try:
            _run(install_command, cwd=FRONTEND_DIR, env=env)
            _run(build_command, cwd=FRONTEND_DIR, env=env)
            return 0
        except subprocess.CalledProcessError as exc:
            print(f"[build.py] frontend build attempt failed with {label}", flush=True)
            last_error = exc
            shutil.rmtree(FRONTEND_DIR / "node_modules", ignore_errors=True)

    assert last_error is not None
    raise last_error


if __name__ == "__main__":
    raise SystemExit(main())
