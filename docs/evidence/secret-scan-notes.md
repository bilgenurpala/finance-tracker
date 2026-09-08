# Secret Scan Notes

Captured on 2026-09-07 during the FinTrack v1 security audit.

## What the scanner reported

Gitleaks 8.30.1 was run against the repository history and the working
directory. Both runs reported zero findings and exited 0. The saved report
(`gitleaks-before-EMPTY-RESULT.json`) contains an empty result set; it is kept as
evidence of what the tool reported, not as evidence that the repository was clean.

## What was actually present

An independent, value-safe inspection of the Git object database found:

- an Anthropic API key in two committed `.pyc` blobs, matching the live key
  format (`sk-ant-api03-` prefix, 109 characters);
- a Flask secret key in one of the same blobs;
- three revisions of a SQLite database holding personal application data.

Secret values, file hashes, and pre-rewrite commit IDs are intentionally
omitted from this document.

## Why the scanner found nothing

The zero-finding report was not a detection gap in the rules. It was a
non-functioning ruleset. Three checks isolated the cause:

| Input | Default ruleset | Explicit `-c` config |
|---|---|---|
| Real key, extracted to plain text | not detected | — |
| Synthetic high-entropy key, correct format | not detected | — |
| `-----BEGIN RSA PRIVATE KEY-----` (literal match, no entropy threshold) | not detected | detected |

The third row settles it. A literal string match is the simplest rule the
tool has. It failed under the default ruleset and succeeded immediately when
a two-rule config file was passed explicitly. No `GITLEAKS_CONFIG` variable
was set and no `.gitleaks.toml` existed in the repository or the home
directory, so nothing was overriding the defaults — they simply were not
loaded.

An earlier draft of this document attributed the miss to binary artifacts
being skipped during diff-based scanning. That explanation was plausible and
wrong; it was written before the control tests above were run.

## Root cause of the exposure itself

`config.py` was added to `.gitignore` after it had already been committed,
and its compiled bytecode was tracked separately. Ignoring a source file does
not untrack artifacts derived from it.

## Takeaways

1. A clean secret-scan report is not evidence of a clean repository. Verify
   the scanner detects a known planted secret before trusting a green result.
2. CI secret scanning needs a canary fixture — a file with a deliberate,
   non-live secret that the pipeline asserts is caught. Without it, a silently
   broken scanner passes every build.
3. Remediation here did not depend on the scanner. History was verified
   directly with `git rev-list --objects --all` and byte-level inspection of
   every blob.

## Status

- History rewrite verified locally and against a fresh mirror clone of the
  remote: the removed paths and the key marker are absent from all reachable
  objects.
- Scanner-based verification is deferred to Phase 2, where a working
  `.gitleaks.toml` and a canary fixture will be added to CI.

## The pre-commit hook is affected too

The `detect-secrets` pre-commit hook reports `Passed` on every commit. A
canary file containing a synthetic key in the correct live format
(`sk-ant-api03-`, 109 characters) was staged and committed successfully with
no warning. The commit was immediately reverted and never pushed.

The hook is therefore not a control at present — it is a green light with
nothing behind it. This is worth stating plainly: between the CI-facing
scanner and the local hook, the repository currently has two secret-scanning
mechanisms and zero secret-scanning coverage.
