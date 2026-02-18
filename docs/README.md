# PsyAI Documentation

This directory contains project documentation (specs, research notes, and architectural details) for PsyAI.

## Directory structure (current)

### `docs/epics/`
Epic and story specifications:
- Epic 1: Centaur integration prototype
- Epic 2: Expert review UI
- Epic 3: Analytics dashboard

## Optional folders (create as needed)

The following folders are referenced in some planning conversations but may not exist yet in the repo. Create them if/when you start adding content of that type:

- `docs/research/` — papers, citations, study design, methodology, analysis plans
- `docs/architecture/` — system design, API specs, DB schemas, diagrams

## Primary research document

The main research outline lives at:

```
Collaborative Writing/psyAI Research Paper - Outline 2.md
```

Use it as the source of truth for:
- Research hypotheses and objectives
- Epic and story definitions
- Requirements and success metrics

## Contributing

When adding docs:
1. Keep terminology consistent with the research outline
2. Prefer clear, testable language (acceptance criteria where applicable)
3. Link to relevant code or issues/PRs
4. Keep docs updated when code changes

## For LLM contributors

Start with `PROJECT_CONTEXT.md` in the repo root for a high-level overview, then jump into `docs/epics/` for the current roadmap.
