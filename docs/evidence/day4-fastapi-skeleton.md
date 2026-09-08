# Day 4 Verification Record — FastAPI Skeleton

Date of work: 2026-09-10 (Phase A, day 4)
Written: 2026-09-11, reconstructed from the working session rather than
captured live. Every row below was observed during the session; none of
the raw tool output was retained. The day 3 and day 5 records were
written the same day and should be preferred as models.

Scope: a running FastAPI application that validates its configuration
and manages database and cache connections. No models, no migrations, no
business logic — those belong to Phase 1.

## What was built

- `app/` package structure: `core/`, `db/models/`, `schemas/`, `api/v1/`,
  `views/`, `services/`, `templates/`, `static/`. The Flask tree was not
  touched.
- `app/core/config.py`: pydantic-settings with `DATABASE_URL`,
  `REDIS_URL`, `SECRET_KEY`, `ENVIRONMENT`, `ANTHROPIC_API_KEY`, `DEBUG`.
  Required fields carry no defaults, so a missing value fails at startup
  instead of silently falling back. `SECRET_KEY` has a minimum-length
  validator; `ANTHROPIC_API_KEY` is optional because the account was
  deleted. Single instance via `lru_cache`.
- `app/db/base.py`: async SQLAlchemy 2.0 engine and `async_sessionmaker`
  factories, plus a Redis connection pool. Connection setup only.
- `app/main.py`: FastAPI instance with a lifespan context manager that
  builds the engine and Redis pool at startup and closes both at
  shutdown. `/docs` and `/redoc` are disabled when
  `ENVIRONMENT=production`.
- `app/core/dependencies.py`: `get_db` and `get_redis`.
- `/health`: issues `SELECT 1` against Postgres and `PING` against Redis,
  returns 200 when both answer and 503 otherwise, naming the failing
  component without leaking connection details.

## Negative controls

| # | Canary | Expectation | Result |
|---|---|---|---|
| 1 | Remove a required variable from `.env` | app fails loudly at startup | failed at startup |
| 2 | Stop the postgres container | `/health` 503, postgres reported unhealthy | as expected |
| 3 | Stop the redis container | `/health` 503, redis reported unhealthy | as expected |
| 4 | Read the 503 response body | no connection string, credentials or exception text | nothing leaked |
| 5 | Start with `ENVIRONMENT=production` | `/docs` returns 404 | 404 |

Control 1 matters because a default value on a required field would have
let the application boot in a half-configured state. Control 4 is the
regression guard for finding #9, where the Flask code returned `str(e)`
to the client.

## Name collision checked before creating the package

A root-level `app.py` already existed. A hypothesis was raised that
adding an `app/` package would shadow it, since packages take precedence
over same-named modules. It was treated as a hypothesis and not acted on
until the decision to stop running Flask through `import app` made it
moot. The file was left in place rather than moved: deleting it early
would have meant import fixes with no payoff.

## Findings

### #17 — .gitignore pattern swallowed the new config file

The `config.py` pattern was unanchored, so it matched
`app/core/config.py` as well as the root file it was written for. The new
config would not have been tracked. Found and fixed the same day by
anchoring the pattern to the repository root.

Same class as finding #1, where `.gitignore` covered `config.py` while
its already-committed `.pyc` carried the secret. In both cases a rule was
written and its coverage was never verified. This is what made
`git check-ignore -v` a standing check on day 5.

### #18 — ValidationError prints every value read from .env

When a required field is missing, the Pydantic `ValidationError` includes
the values of the fields it did read, `.env` contents among them. Visible
in the uvicorn startup traceback and in CI output.

Not a risk on a local machine today. In production, with logs shipped to
an aggregator or an error-tracking service, it exports secrets.
Phase 2: `SecretStr` for sensitive fields and a dedicated handler for
settings load failures.

## Carried to day 5

- `get_settings()` will trip mypy's missing-argument check under
  `lru_cache` + pydantic-settings
- The pre-commit secret hook is installed but, per finding #16, does not
  catch the Anthropic key format — measure the coverage before trusting it
