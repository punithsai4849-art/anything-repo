# SECRETS_EXPOSURE Fix Plan

## Changes

- `.gitignore` — Create standard Python / Django `.gitignore` ignoring `.env`, `*.env.*`, `venv/`, `media/`, `__pycache__/`, `.DS_Store`.
- `cineast_core/settings.py` — Add validation on `SECRET_KEY` so that in production (`DEBUG=False`), it raises an `ImproperlyConfigured` exception if the secret key is missing or insecure.
- `.env.example` — Ensure all environment variables have placeholder values only.

## New files

- `.gitignore`

## Verification goals

After implementation, ALL of these must be true:

- [ ] `.gitignore` exists and explicitly matches `.env`
- [ ] In `DEBUG=False` mode, an insecure/missing `SECRET_KEY` prevents Django startup with `ImproperlyConfigured`
- [ ] No hardcoded live credentials exist in source files
- [ ] `.env.example` contains only placeholder values

## Manual verification (for the human)

- Verify that your actual production `.env` is never committed to any remote repository.
