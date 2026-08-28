# FRONTEND_SECRETS Fix Plan

## Changes

- None required (No frontend secrets exist).

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [x] No secret keys exist in any file under `templates/`, `static/`, or client scripts
- [x] All API interactions from client proxy through server-side routes
- [x] No public environment variables contain sensitive keys

## Manual verification (for the human)

- Inspect browser network dev tools and source tabs on production deployment to verify no unexpected credentials are transmitted in JS bundles.
