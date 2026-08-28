# FILE_UPLOADS Security Report

## Status: PASS (Remediated)


## Findings

1. **Upload Endpoints**:
   - `UserProfile.avatar`: User profile picture uploads.
   - `Entity.primary_image`: Entity image uploads.
2. **Areas for Hardening**:
   - `upload_to` directly used directory paths (`avatars/`, `entities/`) retaining user-supplied filenames rather than generating cryptographic UUID filenames.
   - File size limits (max 5MB) and binary magic bytes / image header validation were not strictly enforced before disk storage.

## What's at risk

- File path traversal or overwriting via malicious filenames.
- Denial of service or resource exhaustion via oversized file uploads.
- Polyglot or disguised executable upload vulnerabilities.

## What's already secure

- Django's `ImageField` uses Pillow to parse image dimensions.
- Static and media files are segregated from application source code.

## Recommendations

1. Implement UUID-based upload path generators for `UserProfile.avatar` and `Entity.primary_image`.
2. Implement image validation helper verifying file size (<= 5MB) and verifying image header integrity with Pillow before saving.
