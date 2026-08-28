# CORS Fix Plan

## Changes

- None required (Same-origin architecture with no wildcard CORS).

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [x] No wildcard CORS origin is emitted
- [x] Cross-origin requests cannot access authenticated endpoints without explicit authorization

## Manual verification (for the human)

- Verify that browser-based cross-origin fetch requests to API endpoints from an unapproved external domain are blocked by CORS policies.
