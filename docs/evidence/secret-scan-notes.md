# Secret Scan Notes

Captured on 2026-09-07 during the FinTrack v1 security audit.
Root-cause section rewritten on 2026-09-08 after further control tests.

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

The default ruleset has no rule for Anthropic API keys. The scanner ran
correctly, loaded its rules, and matched none of them, because none of them
describe the credential that was present.

Control tests, 2026-09-08, gitleaks 8.30.1, default ruleset, no `-c` config:

| Canary | Command | Result |
|---|---|---|
| Complete RSA private key block (`openssl genrsa`) | `gitleaks dir .` | detected — `private-key` |
| Slack bot token, documented format | `gitleaks dir .` | detected — `slack-bot-token` |
| Synthetic `sk-ant-api03-` key, 109 chars, high entropy | `gitleaks dir .` | **not detected** |

The first two rows show the default ruleset loads and matches. The third
isolates the gap to provider coverage.

This is worth stating precisely, because the two failure modes call for
different fixes: a broken scanner is repaired, a missing rule is written.

## Two rejected explanations

Both were plausible, both were wrong, and each was rejected by a test rather
than by argument.

**1. "Binary artifacts are skipped during diff-based scanning."**
Rejected 2026-09-07. Written before any control test was run.

**2. "The default ruleset is not being loaded at all."**
Rejected 2026-09-08. This one survived a day and was recorded as fact, so it
is worth explaining how it passed a control test that should have caught it.

The supporting evidence was a canary containing the literal line
`-----BEGIN RSA PRIVATE KEY-----`, which went undetected under defaults and was
detected with an explicit two-rule config. The inference was that the simplest
possible rule had failed, therefore no rules were loading.

The inference was wrong because the premise was wrong. The built-in
`private-key` rule is not a literal string match — it matches a delimited block,
opening line through closing line. A lone BEGIN line does not satisfy it. The
hand-written rule in `my.toml` was a plain regex, so it matched. Two different
rules, two different behaviours, no evidence about loading either way.

A canary that fails for a reason you have not verified is not a control test.

## The pre-commit hook

The hook is functional. Verified 2026-09-08: a Slack bot token canary was
staged and `pre-commit run gitleaks` returned `Failed`, exit code 1, with the
finding redacted in the output. A commit attempt was blocked.

An earlier note in this document claimed the hook was non-functional, and
commit `27fc459` repeats that claim in its message. Both are incorrect. The
original test used a synthetic `sk-ant-api03-` key, which falls in the same
coverage gap described above — the hook behaved correctly on an input it has
no rule for.

Note that the hook and the CLI are different binaries: the hook uses gitleaks
8.24.2, fetched and cached by pre-commit, while the system CLI is 8.30.1. Both
were tested; both work.

## Root cause of the exposure itself

`config.py` was added to `.gitignore` after it had already been committed,
and its compiled bytecode was tracked separately. Ignoring a source file does
not untrack artifacts derived from it.

## Takeaways

1. A clean secret-scan report is evidence about the ruleset, not about the
   repository. It says nothing about credentials the rules do not describe.
2. Provider coverage is the blind spot to check first. Newer or smaller API
   providers are the ones most likely to be missing from a default ruleset,
   and they are exactly the ones a side project is likely to use.
3. A canary fixture belongs in CI: a deliberate, non-live secret the pipeline
   asserts is caught. Without it, a scanner that covers nothing relevant
   passes every build.
4. Verify what a failed canary actually proves. Read the rule before drawing
   a conclusion from it.
5. Remediation here did not depend on the scanner. History was verified
   directly with `git rev-list --objects --all` and byte-level inspection of
   every blob.

## Status

- History rewrite verified locally and against a fresh mirror clone of the
  remote: the removed paths and the key marker are absent from all reachable
  objects.
- Pre-commit hook verified working against a covered canary.
- Anthropic API keys remain uncovered by the default ruleset. Phase 2 will add
  `.gitleaks.toml` with an `anthropic-api-key` rule and a CI-asserted canary
  fixture.
