# RATE_LIMITING Fix Plan

## Changes

- `cineast_core/ratelimit.py` — Create a rate limiter module utilizing Django cache (`core.cache`) with secure `REMOTE_ADDR` IP extraction.
- `apps/accounts/views.py` — Enforce rate limiting on `login_view` and `register_view`, returning HTTP 429 when throttled.
- `cineast_core/api.py` — Enforce rate limiting on `/api/auth/login` and `/api/auth/register`, returning HTTP 429 when throttled.

## New files

- `cineast_core/ratelimit.py`

## Verification goals

After implementation, ALL of these must be true:

- [ ] Login and registration endpoints are protected by rate limiting
- [ ] Rate limit triggers after 10 attempts within a 15-minute window
- [ ] Rate limiter cannot be bypassed by spoofing `X-Forwarded-For`
- [ ] Rate-limited requests return HTTP status 429
- [ ] Successful attempts or normal traffic under threshold operate without hindrance

## Manual verification (for the human)

- Attempt 11 consecutive failed login attempts from a single client and verify that the 11th request receives HTTP 429 Too Many Requests.
