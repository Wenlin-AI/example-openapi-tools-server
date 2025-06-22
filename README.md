## Overview

This repository provides a reference implementation of **OpenAPI Tool Servers**—lightweight, self-contained HTTP services exposing dummy or example endpoints. It’s designed for rapid experimentation, sandboxed testing (Codex, LLM environments), and integration with AI agents or UIs. You can use this template to:

- Learn how to build a spec-first server with FastAPI
- Package your server for PyPI with the `uv` manager
- Containerize with Docker for one-command deployment
- Integrate with Open WebUI, LangChain, Codex, and more

---

## What are OpenAPI Tool Servers?

**OpenAPI Tool Servers** are dedicated HTTP services that expose a set of RESTful operations described by an OpenAPI specification. They serve as "tools" that AI agents, developer tools, or UIs can programmatically discover and invoke without manual integration work. By adhering to the OpenAPI standard, these servers automatically provide:

- **Machine-readable API definitions** that LLM agents can parse to understand available endpoints, parameter types, and response schemas.
- **Interactive documentation** (Swagger UI, ReDoc) out of the box, aiding both human developers and automated systems in exploring and testing API behavior.
- **Client code generation** support via popular generators (e.g., OpenAPI Generator), speeding up SDK creation in multiple languages.

## Why OpenAPI Tool Servers are Useful

1. **Rapid Prototyping**: Spin up new capabilities by writing spec-first endpoints and stub logic, then immediately test them with AI agents or front-ends.
2. **Interoperability**: Any framework or agent that supports OpenAPI can plug into your tool server—no custom adapters needed.
3. **Consistency & Quality**: OpenAPI enforces clear contracts, parameter validation, and schema definitions, reducing runtime errors and documentation drift.
4. **Security Best Practices**: Leverage standard security schemes (API keys, OAuth2) defined at the spec level, rather than hand-rolling auth flows.
5. **Composable Workflows**: Combine multiple tool servers (e.g., filesystem, Confluence, database) in agent pipelines to build complex tasks without bespoke integrations.

---

## Features

- **OpenAPI-First**: Complete `openapi.yaml` served at `/openapi.json`
- **Interactive Docs**: Swagger UI at `/doc`
- **Stubbed Endpoints**: Prebuilt routers (`/time`, `/echo`, `/math`) returning canned data
- **Packaging**: Managed via `uv` with `pyproject.toml` ready for PyPI
- **Dockerized**: Official `Dockerfile` for quick container builds with examples how you can get your server running with minimal effort
- **Examples**: Integration snippets for Open WebUI, MCPO, LangChain, Langflow and others

---

## Installation & Local Development

You can install directly from the GitHub repository without using a package manager:

```bash
pip install git+https://github.com/your-org/example-openapi-tools-server.git
```

Or, to install and develop locally using `uv`:

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-org/example-openapi-tools-server.git
   cd example-openapi-tools-server
   ```

2. **Install with uv**

   ```bash
   uv install       # Installs dependencies from pyproject.toml
   uv develop       # Editable install for live coding
   ```

3. **Run locally**

   ```bash
   uv run --host 0.0.0.0 --port 8123
   ```

Visit [http://localhost:8123/docs](http://localhost:8123/docs) to explore.

---

## Docker

### Build & Run Locally (Cloned Repo)

```bash
# Build the image from your local copy
docker build -t example-openapi-tools-server .

# Run the container
docker run --rm -p 8123:8123 example-openapi-tools-server
```

Docs remain at `/docs` and `/redoc`.

### Build Directly from GitHub (No Clone)

```bash
# Build image straight from GitHub (uses Docker CLI 18.09+)
docker build -t example-openapi-tools-server \
  "https://github.com/your-org/example-openapi-tools-server.git#main:"

# Run without cloning
docker run --rm -p 8123:8123 example-openapi-tools-server
```

This lets you spin up the example server without any manual cloning or package tooling.

---

## Directory Layout

```
.
├── app/
│   ├── main.py          # FastAPI app
│   └── routers/         # Example stub routers (time, echo, math)
├── docs/                # Requirements & best-practices
│   ├── index.md
│   ├── requirements.md
│   ├── packaging.md
│   ├── docker.md
│   └── testing.md
├── examples/            # Integration snippets
│   ├── openwebui.yaml
│   ├── langchain.py
│   └── codex.md
├── pyproject.toml       # Project metadata + dependencies
├── Dockerfile           # Container setup
└── README.md            # This file
```

---

## Examples

### Open WebUI

```yaml
# examples/openwebui.yaml
tools:
  - name: example
    spec_url: http://localhost:8123/openapi.json
    base_url: http://localhost:8123
```

Launch:

```bash
openwebui --config examples/openwebui.yaml
```

### MCPO (MCP → OpenAPI)

```bash
# Run an MCP stub via mcpo proxy
uvx mcpo --port 8123 -- uvx your-mcp-server
```

Access docs at `http://localhost:8000/docs`.

### LangChain Agent

```python
from langchain.tools import OpenAPITool
from langchain.agents import initialize_agent

tool = OpenAPITool.from_openapi_url(
    name="example",
    url="http://localhost:8123/openapi.json",
)
agent = initialize_agent([tool], llm=your_llm, agent="zero-shot-react-description")
print(agent.run("Return the current time"))
```

---

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## License

MIT © Your Name

