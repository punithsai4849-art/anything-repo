# ACCESS_CONTROL Security Report

## Status: PASS

## Findings

1. **Review Modification & Deletion**:
   - Web view `delete_review_view` checks `review.user != request.user and not request.user.is_staff`.
   - API endpoints `update_review` (`PATCH /api/reviews/{id}`) and `delete_review` (`DELETE /api/reviews/{id}`) explicitly verify `review.user != request.user and not request.user.is_staff` and return HTTP 403 Forbidden.
2. **Ratings Deletion & Creation**:
   - Web view `delete_rating_view` and API `delete_rating` filter deletions strictly scoped to `Rating.objects.filter(user=request.user, entity=entity)`. Users cannot delete or alter ratings belonging to other accounts.
3. **User Profile Modifications**:
   - `edit_profile_view` strictly scopes profile updates to `request.user.profile`.
4. **Community Contributions**:
   - Entity info edits (`/entities/<slug>/edit/`) are community-audited edits recorded in `EntityEditHistory` attributing the authenticated user.

## What's at risk

- Without rigorous ownership verification on resource ID endpoints (IDOR vulnerabilities), malicious users could tamper with or delete other users' reviews, ratings, or profiles.

## What's already secure

- Ownership checks are strictly enforced across reviews, ratings, and profile mutations in both web and REST API layers.
- Admin (`is_staff`) overrides are checked separately from standard user authentication.

## Recommendations

- Enforce `HttpResponseForbidden` (403) on web access control violations in `apps/reviews/views.py`.
