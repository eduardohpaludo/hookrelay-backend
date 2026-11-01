# HookRelay

[![HookRelay CI](https://github.com/eduardohpaludo/hookrelay-backend/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/eduardohpaludo/hookrelay-backend/actions/workflows/ci.yml)

A multi-tenant webhook delivery platform: reliable, secure, observable.

**Status:** early development. The delivery core (v0.1) is done and tested. Work in progress: v0.2, a FastAPI service around it. Queueing, persistence and AWS infrastructure come in later milestones.

## What it does today

**Delivery core.** `send_webhook(url, payload)` posts a JSON payload to a URL and always returns the same structure, whatever happens:

```python
{"ok": bool, "status_code": int | None, "error": str | None, "retryable": bool}
```

The `retryable` flag is the foundation for the retry and dead-letter logic planned for later milestones:

| Outcome | Retryable |
|---|---|
| 2xx | not applicable (`False`) |
| 5xx, 408, 429 | yes |
| Other 4xx | no (permanent) |
| Timeout, connection failure | yes |

**API.** A minimal FastAPI app with `GET /health`, which returns `{"status": "ok"}`.

## Requirements

- [uv](https://docs.astral.sh/uv/) (installs the right Python and the dependencies)
- Git

The Python version (3.14) is pinned in `.python-version` and `pyproject.toml`; see [ADR 001](docs/adr/001-python-version.md). Dependency management is described in [ADR 002](docs/adr/002-uv-for-dependency-management.md).

## Setup

```bash
git clone https://github.com/eduardohpaludo/hookrelay-backend.git
cd hookrelay-backend
uv sync
cp .env.example .env     # Windows: copy .env.example .env
```

`uv sync` creates the virtual environment and installs exactly the versions in `uv.lock`, development tools included.

Edit `.env` and set `WEBHOOK_URL` to an endpoint you control (for example a temporary URL from webhook.site). `.env` is ignored by Git; never commit real URLs or secrets.

## Run

Send a webhook:

```bash
uv run python -m hookrelay_backend.send
```

Example output:

```
Succeeded, Status code: 200
Failed, Status code: 500, Message: 500 Server Error: ..., Retryable: retryable
```

Start the API:

```bash
uv run uvicorn hookrelay_backend.main:app --reload
curl http://127.0.0.1:8000/health
```

## Test and lint

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

The same commands run in CI on every push and pull request, against the locked dependencies (`uv sync --locked`). The `main` branch only accepts changes through a pull request with a passing check.

## Changing dependencies

```bash
uv add <package>          # runtime dependency
uv add --dev <package>    # development-only tool
```

Commit `pyproject.toml` and `uv.lock` together. CI fails if the lock file is out of date.

## Project layout

```
src/hookrelay_backend/   application code (delivery core, API)
tests/                   automated tests (network is mocked)
docs/adr/                architecture decision records
.github/workflows/       CI pipeline
```

Design decisions are recorded as ADRs in [`docs/adr/`](docs/adr/).