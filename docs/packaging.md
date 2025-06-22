# Packaging

The project is managed via a `pyproject.toml` file. Use `uv` to create a
virtual environment and install dependencies before packaging for PyPI:

```bash
uv venv .venv
uv install
```

`uv` automatically detects the `.venv` directory, so activation isn't
necessary.
