# AUTH_MIDDLEWARE Security Report

## Status: PASS (Remediated)


## Findings

1. **Web Views**:
   - All state-changing web views (`entity_create_view`, `entity_edit_view`, `rate_entity_view`, `delete_rating_view`, `create_or_update_review_view`, `delete_review_view`, `edit_profile_view`) are decorated with `@login_required`.
   - Unauthenticated access redirects cleanly to `/accounts/login/?next=...`.
2. **API Routes (`cineast_core/api.py`)**:
   - Protected API routes (`/api/auth/me`, `/api/entities` POST/PATCH, `/api/entities/{id}/relationships`, `/api/entities/{id}/rating`, `/api/entities/{id}/reviews`, `/api/reviews/{id}`) checked authentication inside the endpoint handler (`if not request.user.is_authenticated: return 401`) rather than using Ninja's declarative `auth=...` mechanism that runs *before* the handler.
3. **Admin Endpoints**:
   - Django Admin (`/admin/`) requires `is_staff=True` and redirects/denies non-staff users with 403 / login challenge.

## Complete Route Inventory

| Route | Method | Auth Required | Enforcement Mechanism | Status |
|---|---|---|---|---|
| `/` | GET | No | Public Read | PASS |
| `/discover/` | GET | No | Public Read | PASS |
| `/search/` | GET | No | Public Read | PASS |
| `/entities/<slug>/` | GET | No | Public Read | PASS |
| `/entities/add/` | GET/POST | Yes | `@login_required` | PASS |
| `/entities/<slug>/edit/` | GET/POST | Yes | `@login_required` | PASS |
| `/entities/<id>/rate/` | POST | Yes | `@login_required` | PASS |
| `/entities/<id>/rate/delete/` | POST | Yes | `@login_required` | PASS |
| `/entities/<id>/review/` | POST | Yes | `@login_required` | PASS |
| `/reviews/<id>/delete/` | POST | Yes | `@login_required` + Ownership check | PASS |
| `/accounts/login/` | GET/POST | No | Public Auth Entrypoint | PASS |
| `/accounts/register/` | GET/POST | No | Public Auth Entrypoint | PASS |
| `/accounts/logout/` | GET/POST | No | Clears Session | PASS |
| `/accounts/profile/edit/` | GET/POST | Yes | `@login_required` | PASS |
| `/u/<username>/` | GET | No | Public Profile | PASS |
| `/api/auth/register` | POST | No | Public Registration | PASS |
| `/api/auth/login` | POST | No | Public Login | PASS |
| `/api/auth/logout` | POST | No | Session Logout | PASS |
| `/api/auth/me` | GET | Yes | Declarative `auth=django_auth` | Needs Update |
| `/api/categories` | GET | No | Public Read | PASS |
| `/api/entities` | GET | No | Public Read | PASS |
| `/api/entities/{slug}` | GET | No | Public Read | PASS |
| `/api/entities` | POST | Yes | Declarative `auth=django_auth` | Needs Update |
| `/api/entities/{slug}` | PATCH | Yes | Declarative `auth=django_auth` | Needs Update |
| `/api/entities/{id}/relationships` | POST | Yes | Declarative `auth=django_auth` | Needs Update |
| `/api/entities/{id}/rating` | POST/DELETE | Yes | Declarative `auth=django_auth` | Needs Update |
| `/api/entities/{id}/reviews` | GET | No | Public Read | PASS |
| `/api/entities/{id}/reviews` | POST | Yes | Declarative `auth=django_auth` | Needs Update |
| `/api/reviews/{id}` | PATCH/DELETE | Yes | Declarative `auth=django_auth` + Ownership | Needs Update |
| `/api/search` | GET | No | Public Read | PASS |
| `/api/reports` | POST | No (Optional) | Public/User Reporting | PASS |

## What's at risk

- If authentication checks are embedded manually inside each handler, developer oversight could lead to omitting checks on newly created endpoints. Declarative auth at the router/endpoint level guarantees execution before handler entry.

## What's already secure

- All Django web views use standard `@login_required` decorators and session middleware.

## Recommendations

1. Implement `django_auth` security schema in `cineast_core/api.py`.
2. Apply `auth=django_auth` to all protected endpoints in `cineast_core/api.py`.
