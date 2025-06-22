# Requirements

* **REQ-001**: The server MUST run on Python 3.10 or higher.
* **REQ-002**: Create a virtual environment with `uv` and install the dependencies
  listed in `pyproject.toml`:

  ```bash
  uv venv .venv
  uv pip install .
  ```

  You don't need to activate the environment when running `uv` commands.

## Conventions

### Naming new tool servers

* **REQ-003**: Tools servers MUST be named using the pattern
  `<service>-openapi-tools-server`. For example, a server built for the
  `example` service should be called `example-openapi-tools-server`.

### Unique requirement IDs

* **REQ-004**: Every requirement MUST have a unique identifier so it can be
  tracked and verified. Use the prefix `REQ-` followed by a sequence number
  (for example `REQ-001`, `REQ-002`, and so on).

* **REQ-005**: Tool servers MUST provide a command-line interface to start the
  service. The CLI SHOULD expose `--host` and `--port` options so users can run
  the server after installing it from PyPI or GitHub.

