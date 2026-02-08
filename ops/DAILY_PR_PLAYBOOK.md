# Daily PR Playbook (PsyAI)

Goal: ship **one small PR every night**. Keep it safe, incremental, and reviewable.

## Rules
- PR-only. Never merge automatically.
- Keep changes small (target: **< 150 LOC diff**).
- Prefer **tests/docs/refactor** over new features.
- If tests are slow/heavy, run the smallest meaningful subset.
- Always include:
  - what changed
  - why
  - how to test

## Rotation (choose one each night)
1) Docs-only: clarify README / getting started / architecture notes
2) Tiny code improvement: type hints, small refactor, dead code removal
3) Tests: add/adjust unit test, improve fixture, increase coverage

## Suggested commands
```bash
cd /Users/bonnie/.openclaw/workspace/psyai

git fetch origin

git checkout main

git pull --ff-only

BRANCH="daily-$(date +%Y-%m-%d)"
git checkout -b "$BRANCH"

# make changes

pytest -q

git add -A

git commit -m "Daily: <short summary>"

git push -u origin "$BRANCH"

gh pr create --title "Daily: <short summary>" --body "<what/why/how-to-test>" --base main
```

## Fallbacks
- If tests fail due to env constraints: do docs-only PR.
- If PR already exists for today: skip.
