# ACCESS_CONTROL Fix Plan

## Changes

- `apps/reviews/views.py` — Update `delete_review_view` to return `HttpResponseForbidden` (403) when ownership check fails.

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [ ] Every route with a resource ID parameter checks `current_user.id == resource.owner_id` or `is_staff`
- [ ] Unauthorized modification or deletion attempts return HTTP 403
- [ ] User profile updates cannot alter another user's profile

## Manual verification (for the human)

- Test deleting a review created by User A while logged in as User B and verify 403 rejection.
