# Security

## Current posture

FinTrack is a personal learning project under active remediation. The retained Flask baseline is not production ready and must not be used with real financial records.

## Phase 0 outcome

The September 2026 audit identified a provider key in a tracked compiled Python artifact and a tracked SQLite database containing personal data. The response:

- revoked and replaced the provider credential and JWT signing secret;
- preserved an offline working copy and mirror before rewriting history;
- removed `__pycache__/` and `data/` from the rewritten history;
- force-updated the public branch and verified it with a fresh clone;
- migrated local secrets to ignored `.env` configuration;
- installed a pinned Gitleaks pre-commit hook;
- checked the rewritten history with Gitleaks and an object-level marker search.

No secret value, personal record, historical object ID, or reproduction procedure is included in public evidence.

## Open findings

| Severity | Finding | Planned phase |
|---|---|---|
| Critical | Financial entities lack per-user ownership | Phase 1 |
| Critical | Model output reaches an unsafe HTML sink | Phase 2 |
| Critical | Stored transaction text can cross the prompt instruction boundary | Phase 6 |
| High | Cookie CSRF protection is disabled | Phase 2 |
| High | Destructive routes accept GET | Phase 2 |
| High | Access tokens do not expire and logout has no revocation | Phase 2 |
| High | Mutations do not enforce object ownership | Phases 1–2 |
| High | Login and AI endpoints have no rate limits | Phase 2 |
| High | Debug mode is enabled in the legacy entry point | Phase 2 |
| Medium | Monetary values use floating point | Phase 1 |
| Medium | Schema changes have no migration system | Phase 1 |
| Medium | Budget matching relies on category display names | Phase 1 |
| Medium | Automated tests and CI are absent | Phase 2 |

## Secret handling

- Real values belong only in `.env` or a deployment secret store.
- `.env.example` contains names and non-sensitive defaults only.
- Provider keys are never logged, placed in screenshots, or included in reports.
- Any committed key is considered exposed even after its file is deleted.
- Provider-side rotation is mandatory; history rewriting is insufficient by itself.
- Secret scanning is a guardrail, not proof that a repository is secret-free.

Public evidence is limited to [sanitized code excerpts](evidence/v1-code-snippets.md), [scan notes](evidence/secret-scan-notes.md), and a [hash-free history record](evidence/git-log-v1.txt). Original backups remain offline and must never be pushed or synchronized.

## Reporting a vulnerability

Do not open a public issue containing secrets, personal data, or a working exploit. Use a private GitHub security advisory and provide a minimal sanitized description of the affected component and impact.
