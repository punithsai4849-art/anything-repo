# CSRF Security Report

## Status: PASS (Remediated)


## Findings

1. **CSRF Middleware**:
   - `django.middleware.csrf.CsrfViewMiddleware` is enabled in `MIDDLEWARE` in `cineast_core/settings.py`.
2. **Template Forms**:
   - All 10/10 state-changing POST forms across `templates/` (`login.html`, `register.html`, `edit_profile.html`, `entity_add.html`, `entity_edit.html`, `entity_detail.html` rating/review/report/delete modals, and `base.html` logout) explicitly include `{% csrf_token %}`.
3. **Cookie Attributes**:
   - Explicit settings for `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE`, `CSRF_COOKIE_SAMESITE`, and conditional `SECURE` flags (`not DEBUG`) were not explicitly defined in `settings.py`.

## What's at risk

- Without strict `SameSite=Lax` and `HttpOnly` flags on session cookies, cross-origin requests could attempt to perform authenticated state mutations.

## What's already secure

- All HTML POST forms mandate valid CSRF token validation.
- Standard Django CSRF middleware intercepts and rejects forged POST requests with HTTP 403.

## Recommendations

- Explicitly set session and CSRF cookie flags in `cineast_core/settings.py`:
  - `SESSION_COOKIE_HTTPONLY = True`
  - `SESSION_COOKIE_SAMESITE = 'Lax'`
  - `SESSION_COOKIE_SECURE = not DEBUG`
  - `CSRF_COOKIE_HTTPONLY = False` (or True when not accessed by JS)
  - `CSRF_COOKIE_SAMESITE = 'Lax'`
  - `CSRF_COOKIE_SECURE = not DEBUG`
