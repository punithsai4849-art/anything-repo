# SECURITY_HEADERS Fix Plan

## Changes

- `cineast_core/middleware.py` — Create `SecurityHeadersMiddleware` setting CSP, Referrer-Policy, and HSTS headers.
- `cineast_core/settings.py` — Register `cineast_core.middleware.SecurityHeadersMiddleware` and configure `SECURE_REFERRER_POLICY`, `SECURE_HSTS_SECONDS`.

## New files

- `cineast_core/middleware.py`

## Verification goals

After implementation, ALL of these must be true:

- [ ] `Content-Security-Policy` header present on every HTTP response
- [ ] `Referrer-Policy: strict-origin-when-cross-origin` present on every response
- [ ] `X-Frame-Options: DENY` present on every response
- [ ] `X-Content-Type-Options: nosniff` present on every response
- [ ] Headers are applied via a single global middleware

## Manual verification (for the human)

- Run `curl -I http://127.0.0.1:8000/` and verify all security headers.
