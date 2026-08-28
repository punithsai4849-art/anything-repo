# CSRF Fix Plan

## Changes

- `cineast_core/settings.py` — Add explicit `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SAMESITE`, `CSRF_COOKIE_SECURE` configuration.

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [ ] `SESSION_COOKIE_HTTPONLY` is set to `True`
- [ ] `SESSION_COOKIE_SAMESITE` is set to `'Lax'`
- [ ] `CSRF_COOKIE_SAMESITE` is set to `'Lax'`
- [ ] `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` are enabled when `DEBUG=False`
- [ ] Cross-origin POST without CSRF token fails with 403

## Manual verification (for the human)

- Test a cross-origin form POST without CSRF token from another domain and verify 403 rejection.
