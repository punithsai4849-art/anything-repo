# RATE_LIMITING Security Report

## Status: PASS (Remediated)


## Findings

1. **Missing Rate Limiting on Authentication**:
   - Web authentication endpoints (`login_view`, `register_view` in `apps/accounts/views.py`) and API endpoints (`/api/auth/login`, `/api/auth/register` in `cineast_core/api.py`) lacked rate limiting.
   - An automated attacker could attempt brute-force password guessing or spam user registrations without throttling.
2. **IP Resolution**:
   - Must strictly use `request.META['REMOTE_ADDR']` to prevent header spoofing via untrusted `X-Forwarded-For` headers.

## What's at risk

- Credential stuffing and password brute-force attacks against user accounts.
- Automated bulk account creation and resource exhaustion.

## What's already secure

- Passwords are verified server-side with standard Django password hashing.

## Recommendations

1. Implement `cineast_core/ratelimit.py` providing robust cache-backed rate limiting per IP and action (10 attempts per 15 minutes).
2. Integrate rate limiting into `apps/accounts/views.py` (`login_view`, `register_view`) returning HTTP 429 Too Many Requests.
3. Integrate rate limiting into `cineast_core/api.py` (`/api/auth/login`, `/api/auth/register`) returning HTTP 429 Too Many Requests.
