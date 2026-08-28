# DATABASE_ACCESS Fix Plan

## Changes

- None required (Architecture uses server-side Django ORM with no direct client-side DB access).

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [x] No client-side database connections exist in frontend or public assets
- [x] Database credentials only load server-side in `settings.py`
- [x] All database mutations happen via server-side Django models and views

## Manual verification (for the human)

- Ensure PostgreSQL database user permissions on production follow the principle of least privilege.
