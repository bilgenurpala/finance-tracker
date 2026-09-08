# Tooling Coverage Measurement

Date: 2026-09-11 (Phase A, day 5)
Purpose: measure what the quality gates actually catch, before relying on
them in Phase 1. Nothing here is a fix — remediation belongs to Phase 2.

Rule: a tool is only trusted once a deliberately broken input has been
shown to trigger it. A green run on clean input proves nothing.

## Environment

| Tool | Version |
|---|---|
| uv | 0.12.10 |
| Python | 3.12.14 |
| ruff | 0.16.6 |
| mypy | 2.3.1 |
| pytest | 9.1.1 |
| pre-commit | 4.6.2 |
| gitleaks | v8.30.0 |
| pre-commit-hooks | v6.0.0 |

## 1. Dependency groups (uv)

Canary: run `uv sync --no-default-groups` and inspect `.venv/bin`
directly, not through `uv run` (which re-syncs the environment first and
would mask the result).

| Expectation | Result |
|---|---|
| ruff, mypy, pytest absent | absent |
| flask absent | absent |
| fastapi present | present |
| `app.main` imports with flask absent | imports |

The last row is the one that matters for 2026-09-28: `app/` does not
depend on the Flask tree.

## 2. ruff

Canary file in `app/` containing an unused import, a `subprocess` call
with `shell=True`, and a 122-character line.

| Rule | Result |
|---|---|
| F401 unused import | caught |
| S602 shell=True | caught |
| E501 line too long | caught |

Reverse direction: the same file placed in `src/` produced no output,
including when its path was passed explicitly. `force-exclude = true`
holds under pre-commit, which passes filenames explicitly.

### Finding: ruff 0.16 formats Markdown

ruff 0.16 reformats Python code blocks inside `.md` files by default.
This rewrote `docs/evidence/v1-code-snippets.md`, which records v1 code
as it was originally written. Scoping `[tool.ruff.format] exclude` to
`["docs"]` did not stop it; `["*.md"]` did.

`ruff check` never reads Markdown — only the formatter does. A green
`ruff check` says nothing about code blocks in documentation.

## 3. mypy

Canary: a function returning `str` from a signature declaring `int`, and
an `int` passed to a `str` parameter.

| Rule | Result |
|---|---|
| return-value | caught |
| arg-type | caught |

### Finding: mypy has no force-exclude

`files = ["app"]` applies only when mypy runs with no arguments. The same
canary placed in `src/` was still checked when its path was passed
explicitly. Because pre-commit passes filenames, the mypy hook is scoped
with `files: ^app/`. Without that, every commit would surface errors from
the Flask code that is being removed anyway.

### Known gap

`tests/` is outside the mypy scope (`files = ["app"]`). Deliberate for
now. Phase 2.

## 4. pytest

| Canary | Expectation | Result |
|---|---|---|
| Expected status changed 200 -> 418 | suite turns red | red |
| Test file renamed without `test_` prefix | not collected | 3 collected, not 6 |
| Integration test with postgres stopped | fails | ConnectionRefusedError |
| Integration test with postgres running | passes | passes |

### Finding: a green test that verified the wrong thing

`test_missing_required_field_raises` originally asserted that the field
name appeared in the `ValidationError` text. Three of the four required
fields have validators that fire before the missing-field check, so the
assertion matched an unrelated error message and passed for the wrong
reason. Only `REDIS_URL`, which has no validator, exposed it.

Found by breaking the `clean_env` fixture — replacing `delenv` with
`setenv` — and reading *which* parametrised cases failed rather than only
that some did. The assertion now checks the structured error type
(`e["type"] == "missing"`), and all four cases fail under the same canary.

The lesson generalises: a negative control that turns red is not enough.
The shape of the red matters.

### Finding: /health does not degrade when Postgres is down at startup

With Postgres stopped, the integration test failed with
`ConnectionRefusedError` during lifespan startup rather than returning
503. The degraded path is only reachable when the dependency fails after
the app is up. Not investigated today. Phase 2.

## 5. Secret scanning — measurement of finding #16

Canaries are invalid strings generated for this test. No real credential
was used.

| Input | gitleaks | detect-private-key |
|---|---|---|
| Anthropic `sk-ant-api03-...` | missed | missed |
| AWS official example key (`AKIAIOSFODNN7EXAMPLE`) | missed | missed |
| AWS randomly generated key | caught | missed |
| Generic `API_KEY=...` | caught | missed |
| RSA private key block | caught | caught |

The first AWS miss is not a gap in gitleaks: `AKIAIOSFODNN7EXAMPLE` is
AWS's published documentation value and is allow-listed. A randomly
generated AWS key is caught. The canary was at fault, not the tool —
which is itself a result worth recording, because an allow-listed sample
would have been read as a failure.

**Finding #16 confirmed and narrowed:** gitleaks v8.30.0 default rules do
not recognise the Anthropic API key format. That is precisely the
credential class that leaked into this repository in March 2026. A custom
`.gitleaks.toml` with an `anthropic-api-key` rule, plus a CI canary, is
Phase 2 work.

Note: `detect-private-key` catches the RSA block that gitleaks defaults
also catch, and nothing else. It is a narrow second opinion, not a
general secret scanner.

## 6. .gitignore coverage — measurement of finding #17

Verified with `git check-ignore -v`, per path, rather than assuming the
patterns cover what they were written for.

| Path | Result |
|---|---|
| `.env` | ignored (`.gitignore:6`) |
| `data/finance.db` | ignored (`.gitignore:9`) |
| `app/__pycache__/*.pyc` | ignored (`.gitignore:1`) |
| `.coverage` | ignored (`.gitignore:28`) |
| `.pytest_cache/` | ignored (`.gitignore:31`) |
| `settings.py` | not ignored (correct) |
| `app/core/config.py` | not ignored (correct) |

Both directions checked: the patterns cover the generated files and do
not swallow real source.

### Third recurrence of finding #17

`.coverage` was committed earlier the same day, in the commit that added
the test suite. An ignore rule existed for caches but did not cover
newly generated artefacts. Removed from tracking and the pattern added.

This is the same class as finding #1 (a `.gitignore` covering
`config.py` while its compiled `.pyc` was already committed) and finding
#17 (a pattern that swallowed the new config file). Writing the rule and
verifying its coverage are different acts.

## 7. pre-commit gate

| Canary | Result |
|---|---|
| File with lint error and no return annotation | commit blocked by ruff-check, ruff-format and mypy |
| 9.7 MB binary | commit blocked by check-added-large-files |

Verified that no commit object was created in the blocked case.

## Carried to Phase 2

- #16 custom `.gitleaks.toml` with an `anthropic-api-key` rule, plus a CI canary
- #17 keep `git check-ignore -v` as a repeatable check, not a one-off
- #18 SecretStr for sensitive Settings fields and a dedicated handler for load failures
- mypy coverage for `tests/`
- `/health` degraded path when a dependency is down at startup
