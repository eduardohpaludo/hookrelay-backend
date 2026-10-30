# HookRelay

[![HookRelay CI](https://github.com/eduardohpaludo/hookrelay-backend/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/eduardohpaludo/hookrelay-backend/actions/workflows/ci.yml)

A multi-tenant webhook delivery platform: reliable, secure, observable.

**Status:** v0.1, early development. Today the repository contains the delivery core: a function that sends a signed-off webhook payload, classifies every failure as retryable or permanent, and is covered by automated tests and CI. The API, queueing and AWS infrastructure come in later milestones.

## What it does today

`send_webhook(url, payload)` posts a JSON payload to a URL and always returns the same structure, whatever happens:

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

## Requirements

- Python 3.14 (see [ADR 001](docs/adr/001-python-version.md))
- Git

## Setup

```bash
git clone https://github.com/eduardohpaludo/hookrelay-backend.git
cd hookrelay-backend
python -m venv .venv
```

Activate the virtual environment:

```bash
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Install dependencies and configure the target URL:

```bash
pip install -r requirements-dev.txt
cp .env.example .env     # Windows: copy .env.example .env
```

Edit `.env` and set `WEBHOOK_URL` to an endpoint you control (for example a temporary URL from webhook.site). `.env` is ignored by Git; never commit real URLs or secrets.

## Run

```bash
python send.py
```

Example output:

```
Succeeded, Status code: 200
Failed, Status code: 500, Message: 500 Server Error: ..., Retryable: retryable
```

## Test and lint

```bash
python -m pytest
ruff check .
ruff format --check .
```

The same three commands run in CI on every push and pull request. The `main` branch only accepts changes through a pull request with a passing check.

## Roadmap

1. Local script, tests and CI (this release)
2. FastAPI service with endpoint registration, delivery and Docker
3. Deployment on AWS with Terraform and OIDC
4. Queue, dead-letter queue and delivery history
5. Retries with backoff, HMAC signing, SSRF protection, circuit breaker, rate limiting
6. Multi-account platform and promotion pipeline
7. Observability, SLOs and load tests
8. Multi-tenancy and multi-region disaster recovery
9. Architecture documentation

Design decisions are recorded as ADRs in [`docs/adr/`](docs/adr/).