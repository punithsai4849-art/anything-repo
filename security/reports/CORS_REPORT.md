# CORS Security Report

## Status: PASS

## Findings

1. **Monolithic Origin Model**: The application serves both web views and REST API endpoints under the same origin.
2. **No Wildcard Headers**: No `Access-Control-Allow-Origin: *` headers or unvetted CORS middlewares are configured.
3. **Credentials Isolation**: Cross-origin requests cannot transmit session cookies or execute state modifications without explicit CSRF/CORS authorization.

## What's at risk

- Wildcard CORS with credentials would permit untrusted websites to send authenticated requests on behalf of logged-in users and read sensitive API data.

## What's already secure

- Same-origin architecture with strict SameSite cookies ensures cross-origin isolation.

## Recommendations

- If a separate frontend domain is introduced in the future, use `django-cors-headers` with an explicit `CORS_ALLOWED_ORIGINS` domain allowlist and never `CORS_ALLOW_ALL_ORIGINS = True`.
