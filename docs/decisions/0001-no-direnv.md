# 0001 — No direnv for environment variables

Date: 2026-09-08
Status: Accepted

## Context

The Phase A checklist included installing direnv to auto-load environment
variables on directory entry. Meanwhile, the application already reads `.env`
through pydantic-settings, a change made during Phase 0.

## Decision

Skip direnv. `.env` + pydantic-settings is the single source of configuration.

## Rationale

- Two loading paths create precedence ambiguity: pydantic-settings prefers a
  shell environment variable over the `.env` file, so an edited `.env` could be
  silently ignored.
- direnv exports secrets into the shell environment, where every child process
  started from that shell can read them. pydantic-settings keeps them in the
  application process only.
- Docker Compose (Phase A, day 3) reads `.env` directly, so direnv adds nothing
  there either.

## Consequences

- `.envrc` and `.direnv/` are still gitignored in case the tool is introduced later.
- Anyone running the app outside the application entrypoint must load `.env`
  themselves.
