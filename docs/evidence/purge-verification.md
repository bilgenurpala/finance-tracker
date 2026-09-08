# History Purge Verification

Date: 2026-09-09
Verifier: repository owner
Scope: independent verification of the `git filter-repo` cleanup performed on 2026-09-07.

## What was searched

Six targets, none of which are reproduced in this document:

| # | Target | Type |
|---|---|---|
| 1 | Old application SECRET_KEY | content pattern |
| 2 | Account email address stored in the committed database | content pattern |
| 3 | Second email address found in the same database | content pattern |
| 4 | bcrypt hash prefix | content pattern |
| 5 | `data/finance.db` | path |
| 6 | `__pycache__/` and `*.pyc` | path |

Patterns were kept in a mode-600 file outside the repository and read by the
scan script at runtime, so they never appear in shell history or in this file.

## Method

A standalone script enumerated every object in each repository and searched
blob contents directly, independently of gitleaks:

- `git cat-file --batch-all-objects` for content search — this covers objects
  that are unreachable from any ref, which `git rev-list --all` would miss.
- `git rev-list --objects --all` for path search, since filenames only exist
  in tree objects.
- `grep -aF` so that binary blobs (the SQLite database, compiled `.pyc`) are
  searched as bytes rather than skipped as binary.

gitleaks was deliberately not used. On 2026-09-08 a controlled canary test
showed its default ruleset does not detect the key format involved, so a clean
gitleaks run would have carried no evidential value here.

## Negative control

Before trusting any "not found" result, the same script was run against the
pre-cleanup bare backup taken on 2026-09-07.

Result: all six targets were found there. The method detects what it claims to
detect, so a "not found" elsewhere is meaningful.

An earlier run of this control returned NOT FOUND for one email pattern. The
cause was an incorrect pattern supplied from memory, not a defect in the search
method — the correct value was extracted from the blob itself and the control
was re-run to completion.

## Results

| Repository | Path targets | Content targets |
|---|---|---|
| Pre-cleanup backup (control) | found | found |
| Working clone | not found | not found |
| Fresh `--mirror` clone of the remote | not found | not found |

Object counts: 88 blobs in the backup, 91 in the working clone (includes
unreachable objects left by filter-repo), 86 in the fresh mirror.

## Finding: the mirror clone was not sufficient

A `--mirror` clone only fetches objects reachable from refs. Force-pushing does
not delete the old objects on GitHub; it only detaches them from a branch.

Three pre-cleanup commit SHAs were recovered from the backup and requested
directly:

- `https://github.com/<owner>/<repo>/commit/<sha>` rendered the old tree,
  including `data/finance.db` and `__pycache__/config.cpython-312.pyc`.
- `https://raw.githubusercontent.com/<owner>/<repo>/<sha>/data/finance.db`
  returned HTTP 200 and a valid 40 KB SQLite file matching the search patterns.

So the cleanup was incomplete on the server side, and the clean mirror result
alone would have been a false assurance.

## Remediation

Fork count, star count, watcher count and open issue count were all zero, so no
objects had propagated to a fork network.

The repository was renamed to `finance-tracker-v1-archive` and made private.
Development continues in a new public repository with clean history.

## Verification of the remediation

| Check | Result |
|---|---|
| Old SHA on old repo name, previously requested file | 404 |
| Old SHA on old repo name, never-requested file | 404 |
| `main` branch on old repo name | 404 |
| Repository HTML page on old repo name | 404 |
| Old SHA on new repo name | 404 |
| Unauthenticated API, both names | 404 |

Immediately after the visibility change, one URL still returned 200: the exact
file requested repeatedly during earlier testing. Header inspection showed
`x-cache: HIT` with `max-age=300`.

Five consecutive requests returned 200 from five different `x-served-by` nodes,
which was briefly taken as evidence that the origin was still serving the file.
That reading was wrong: all five nodes were in the same Fastly POP
(`x-github-edge-region: fra`) and shared an upstream shield cache.

The decisive test was requesting a file at the same old SHA that had never been
fetched before. It returned 404, as did the repository page and `main`. The
lone 200 was therefore a cache entry created by the testing itself, and it
expired on schedule.

Lesson: when several observations share a common upstream, they are one
observation. The discriminating test is the one that varies the input, not the
one that repeats it.

## Known limitation

This is an access-control remediation, not deletion. The objects still exist in
GitHub's storage for the archived repository. Making that repository public
again would make the same SHAs retrievable.

Claims about this cleanup should be worded accordingly: history was rewritten
and public access was closed, not that the objects were destroyed.

## Residual risk

The exposed API key and SECRET_KEY are both dead. What remained retrievable was
an email address and a bcrypt hash with cost factor 12.
