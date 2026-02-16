# Quick checks (lightweight)

This project has a few fast sanity checks that are useful before opening a PR.

## 1) Python syntax / import sanity

From the repo root:

```bash
python -m compileall src
```

This catches basic syntax errors across the `src/` tree without running the app.

## 2) Unit tests (when available)

If your environment is set up for tests:

```bash
pytest -q
```

If tests fail due to missing external services or local env constraints, prefer a
**docs-only** PR rather than weakening test coverage.

## 3) Keep diffs small

For routine maintenance PRs, aim for:

- No behavior changes unless clearly intended
- Minimal new dependencies
- Focused diffs (roughly <150 LOC)

## 4) Helpful PR description

Include:

- What changed (bullets)
- Why (motivation)
- How to test (commands or manual steps)
