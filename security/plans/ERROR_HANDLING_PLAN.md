# ERROR_HANDLING Fix Plan

## Changes

- `cineast_core/api.py` — Add `@api.exception_handler(Exception)` to sanitize unexpected exceptions and return generic `{"detail": "Internal server error"}` with HTTP 500.
- `templates/404.html` — Neubrutalist clean 404 page.
- `templates/500.html` — Neubrutalist clean 500 error page.

## New files

- `templates/404.html`
- `templates/500.html`

## Verification goals

After implementation, ALL of these must be true:

- [ ] Unhandled API exceptions return HTTP 500 with generic JSON `{ "detail": "Internal server error" }`
- [ ] No stack traces, file paths, or SQL queries are exposed to clients
- [ ] Custom 404 and 500 error pages render cleanly

## Manual verification (for the human)

- Test hitting a non-existent URL (e.g. `/not-found-12345/`) and verify the 404 page renders without technical details.
