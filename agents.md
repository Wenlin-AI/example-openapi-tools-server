# AGENTS.md

> **Note for AI assistants and human maintainers**\
> Lines or tokens annotated with `` (or labelled `(EXAMPLE)` inside strings) are *illustrative placeholders* that **MUST be replaced** with project‑specific values when you generate or extend a real repo.

## 1  Purpose

This file instructs AI coding assistants (e.g. OpenAI Codex, Gemini CLI, Claude Code) how to bootstrap **a brand‑new FastAPI “tool‑server” project** from an empty repository. When the assistant finishes, the repository should:

1. Target **Python ≥ 3.12**.
2. Contain **all source code inside an **``** folder**.
3. Expose a fully generated **OpenAPI spec at **`` (no hand‑written `openapi.yaml`).
4. Listen on `` by default.
5. Be **Docker‑ and Docker‑Compose‑ready** for one‑command deployment from GitHub.
6. Ship with **pytest tests**, **GitHub Actions CI**, and code‑quality tooling (Black, isort, flake8, MyPy).

## 2  Quick‑Start Checklist for the Agent

1. **Generate project layout** exactly as shown in § 3.
2. **Populate every file** with minimal yet functional code/templates in § 4.
3. **Add Poetry‑managed **`` with all dependencies from § 5.
4. **Create a **``** & **`` per § 6.
5. **Scaffold CI workflow** in `.github/workflows/ci.yml` (§ 7).
6. **Commit everything**; no manual steps should remain for the human maintainer.

## 3  Project Layout

```text
/
├── AGENTS.md                ← this file
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml           ← Poetry project file
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   ├── main.py              ← creates FastAPI app & uvicorn runner
│   ├── cli.py               ← Typer CLI wrapper around main.run()
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py        ← GET /health
│   │   ├── time.py          ← GET /time  # (EXAMPLE‑router)
│   │   ├── echo.py          ← POST /echo # (EXAMPLE‑router)
│   │   └── math.py          ← POST /math/sum # (EXAMPLE‑router)
│   └── services/            ← utility modules (optional)
├── tests/
│   ├── __init__.py
│   └── test_health.py
└── docs/                    ← human‑readable API docs / reference material
```

## 4  File‑by‑File Requirements

### 4.1 `app/main.py`

```python
from typing import Annotated

import uvicorn
from fastapi import FastAPI

from app.routers import health, time, echo, math

app = FastAPI(
    title="Example Tool Server",  # (EXAMPLE)
    version="0.1.0"                # (EXAMPLE)
)
app.include_router(health.router)
app.include_router(time.router)   # (EXAMPLE)
app.include_router(echo.router)   # (EXAMPLE)
app.include_router(math.router)   # (EXAMPLE)


def run(
    host: Annotated[str, "server host"] = "0.0.0.0",
    port: Annotated[int, "server port"] = 8888,
    reload: bool = False,
):
    """Entrypoint used by Typer CLI and docker‑compose."""
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)

if __name__ == "__main__":
    run()
```

### 4.2 `app/cli.py`

```python
import typer
from app.main import run

cli = typer.Typer(help="Command‑line interface for the tool server")

@cli.command()
def serve(
    host: str = "0.0.0.0",
    port: int = 8888,
    reload: bool = False,
):
    """Start HTTP server."""
    run(host, port, reload)

if __name__ == "__main__":
    cli()
```

### 4.3 Routers

Each router exposes a minimal endpoint and must declare `tags` for OpenAPI grouping.

Example (`health.py`):

```python
from fastapi import APIRouter

router = APIRouter(prefix="", tags=["health"])

@router.get("/health")
async def health():
    """Simple heartbeat endpoint."""
    return {"status": "ok"}
```

Additional illustrative routers:

```python
# time.py (EXAMPLE)
from datetime import datetime
from fastapi import APIRouter

router = APIRouter(prefix="", tags=["time"])

@router.get("/time")
async def current_time():
    return {"now": datetime.utcnow().isoformat()}
```

```python
# echo.py (EXAMPLE)
from fastapi import APIRouter
from pydantic import BaseModel

class EchoBody(BaseModel):
    message: str

router = APIRouter(prefix="", tags=["echo"])

@router.post("/echo")
async def echo(body: EchoBody):
    return body
```

```python
# math.py (EXAMPLE)
from fastapi import APIRouter
from pydantic import BaseModel

class Numbers(BaseModel):
    a: float
    b: float

router = APIRouter(prefix="/math", tags=["math"])

@router.post("/sum")
async def add(body: Numbers):
    return {"result": body.a + body.b}
```

### 4.4 `tests/test_health.py`

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

# Additional example test  (EXAMPLE)
# def test_time():
#     resp = client.get("/time")
#     assert resp.status_code == 200
```

### 4.5 `.gitignore`

Include typical Python, Poetry, and Docker exclusions (e.g., `__pycache__/`, `.venv/`).

### 4.6 `.dockerignore`

Exclude `.git`, `tests/`, `docs/`, and local env files for slimmer images.

## 5  Dependencies (`pyproject.toml`)

Use **Poetry** for dependency management.

```toml
[tool.poetry]
name = "example-openapi-tool-server"   # (EXAMPLE)
version = "0.1.0"                      # (EXAMPLE)
description = "Scaffolded FastAPI tool server"  # (EXAMPLE)
authors = ["<YOUR NAME>"]             # (EXAMPLE)

[tool.poetry.dependencies]
python = "^3.12"
fastapi = "^0.111"
uvicorn = {extras = ["standard"], version = "^0.30"}
typer = "^0.12"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
black = "^24.4"
isort = "^5.13"
flake8 = "^7.0"
mypy = "^1.10"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 6  Docker & Compose

### 6.1 `Dockerfile`

```dockerfile
FROM python:3.12-slim
WORKDIR /srv/app
COPY pyproject.toml poetry.lock* /srv/app/
RUN pip install --no-cache-dir poetry && poetry install --no-root --no-dev
COPY . /srv/app
EXPOSE 8888
CMD ["poetry", "run", "python", "app/cli.py", "serve", "--host", "0.0.0.0", "--port", "8888"]
```

### 6.2 `docker-compose.yml`

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8888:8888"
    environment:
      PYTHONUNBUFFERED: "1"
```

## 7  CI — GitHub Actions (`.github/workflows/ci.yml`)

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install poetry
      - run: poetry install
      - run: poetry run black --check .
      - run: poetry run isort --check-only .
      - run: poetry run flake8
      - run: poetry run mypy app
      - run: poetry run pytest -q
```

## 8  Style & Quality Gates

- **Formatting:** run `poetry run black .` and `poetry run isort .` before committing.
- **Linting:** `poetry run flake8` must pass in CI.
- **Type‑checking:** `poetry run mypy app` must report zero errors.

## 9  Extending the Server

1. Add new routers in `app/routers/`—FastAPI auto‑discovers them if imported.
2. Update tests accordingly.
3. Docker image rebuilds automatically via Compose or CI pipeline.

---

**End of AGENTS.md**

