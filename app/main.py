from fastapi import FastAPI
from .routers import time, echo, math
import yaml
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SPEC_PATH = os.path.join(BASE_DIR, "openapi.yaml")

app = FastAPI(openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc")

# Load OpenAPI spec from YAML file and use it for the /openapi.json route
with open(SPEC_PATH, "r") as f:
    openapi_schema = yaml.safe_load(f)


@app.on_event("startup")
async def log_docs_url() -> None:
    """Log the documentation URL when the app starts."""
    host = os.getenv("SERVER_HOST", "127.0.0.1")
    port = os.getenv("SERVER_PORT", "8123")
    logger = logging.getLogger("uvicorn")
    logger.info("Docs available at http://%s:%s%s", host, port, app.docs_url)

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_spec():
    return openapi_schema

app.include_router(time.router)
app.include_router(echo.router)
app.include_router(math.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8123)))
