# PASSWORD_HASHING Security Report

## Status: PASS (Remediated)


## Findings

1. **Hashing Algorithm**:
   - Django uses PBKDF2 with SHA-256 (`PBKDF2PasswordHasher`) with 870,000+ work iterations by default.
   - Passwords stored in `auth_user` table are hashed with unique random salt per user.
   - Zero MD5, SHA-1, or plaintext storage exists.
2. **Password Length Validation**:
   - `MinimumLengthValidator` in `settings.py` was previously configured to `min_length: 6`.
   - Security best practices mandate a minimum password length of at least 8 characters.

## What's at risk

- Short passwords (< 8 chars) are vulnerable to dictionary and rainbow table cracking if password hashes are ever leaked.

## What's already secure

- Cryptographic PBKDF2-SHA256 hashing with per-user salt.
- Built-in protection against common passwords and numeric-only passwords.

## Recommendations

1. Update `MinimumLengthValidator` `min_length` to `8` in `cineast_core/settings.py`.
2. Explicitly define `PASSWORD_HASHERS` in `cineast_core/settings.py`.
