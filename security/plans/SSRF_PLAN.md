# SSRF Fix Plan

## Changes

- None required (No user-supplied URL fetching exists on the server).

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [x] No backend functions execute arbitrary HTTP/HTTPS requests based on user input
- [x] Internal/loopback interfaces are not reachable through application endpoints

## Manual verification (for the human)

- If external scraping features are added in future iterations, ensure SSRF protections are implemented.
