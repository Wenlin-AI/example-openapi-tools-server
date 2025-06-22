import uvicorn
import typer


def main(host: str = "127.0.0.1", port: int = 8123) -> None:
    """Start Example OpenAPI Tools Server."""
    uvicorn.run("app.main:app", host=host, port=port)


def entrypoint() -> None:
    typer.run(main)


if __name__ == "__main__":
    entrypoint()
