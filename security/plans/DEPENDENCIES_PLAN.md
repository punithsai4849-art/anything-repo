# DEPENDENCIES Fix Plan

## Changes

- `requirements.txt` — Pin exact versions for all direct dependencies.

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [ ] All packages in `requirements.txt` are pinned with exact versions (`==`)
- [ ] No unpinned ranges (`>=`, `^`, `~`) remain in `requirements.txt`
- [ ] All test suites pass cleanly with pinned dependencies

## Manual verification (for the human)

- Run `pip install -r requirements.txt` in a fresh environment to ensure deterministic dependency resolution.
