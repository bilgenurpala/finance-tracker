# Secret Scan Notes

Captured on 2026-09-07 during the FinTrack v1 security audit.

## Before history rewrite

Gitleaks v8.24.2 scanned the full working-directory backup and reported zero
findings. The original JSON output is preserved in `gitleaks-before.json`.

An independent, value-safe check found:

- one Anthropic API key marker in the compiled Python configuration file;
- one 40,960-byte SQLite database containing personal application data.

Secret values, personal records, file hashes, and historical commit object IDs
are intentionally omitted.

## Interpretation

The zero-finding Gitleaks report was a false negative for this repository.
The exposed credential was stored in a compiled Python file, and its key format
was not detected by the scanner's default directory-scan behavior.

This demonstrates that secret scanning is a guardrail, not proof that a
repository contains no secrets. Ignore rules, tracked-file inspection, binary
artifacts, and Git history must also be reviewed.

## After history rewrite

The rewritten ten-commit history was scanned with Gitleaks v8.24.2 and reported
no leaks. A separate object-level search also confirmed that the Anthropic key
marker and the removed `data/` and `__pycache__/` paths were absent.
