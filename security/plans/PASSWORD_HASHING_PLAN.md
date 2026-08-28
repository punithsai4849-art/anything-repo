# PASSWORD_HASHING Fix Plan

## Changes

- `cineast_core/settings.py` — Increase `MinimumLengthValidator` `min_length` to 8 and define `PASSWORD_HASHERS`.

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [ ] Password hashing uses PBKDF2 SHA-256 or Argon2
- [ ] Minimum password length validation enforces at least 8 characters
- [ ] Passwords shorter than 8 characters are rejected during registration

## Manual verification (for the human)

- Attempt to register a user with a 6-character password and confirm validation rejection.
