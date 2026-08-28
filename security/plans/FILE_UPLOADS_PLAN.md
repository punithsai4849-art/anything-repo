# FILE_UPLOADS Fix Plan

## Changes

- `apps/accounts/models.py` — Add `avatar_upload_path` using `uuid.uuid4()`.
- `apps/entities/models.py` — Add `entity_image_upload_path` using `uuid.uuid4()`.
- `apps/accounts/views.py` & `apps/entities/views.py` — Enforce file size limit (5MB) and image verification.

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [ ] Uploaded files are renamed to UUIDs server-side
- [ ] Non-image files or corrupted binary payloads are rejected
- [ ] File size limit of 5MB is strictly enforced server-side

## Manual verification (for the human)

- Upload a profile avatar and check the `media/avatars/` directory to confirm the file is saved as `<uuid4>.<ext>`.
