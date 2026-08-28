# AUTH_MIDDLEWARE Fix Plan

## Changes

- `cineast_core/api.py` — Import `django_auth` from `ninja.security` and apply `auth=django_auth` to all protected endpoints (`/auth/me`, `/entities` POST/PATCH, `/entities/{id}/relationships`, `/entities/{id}/rating`, `/entities/{id}/reviews`, `/reviews/{id}`).

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [ ] Every route modifying or returning sensitive user data has auth middleware running before handler entry
- [ ] Unauthenticated API requests to protected endpoints return 401 with standard Ninja error response
- [ ] Web requests to protected views redirect to `/accounts/login/`
- [ ] Authenticated requests continue functioning as expected

## Manual verification (for the human)

- Test making a POST request to `/api/entities` without a session cookie and verify immediate 401 response.
