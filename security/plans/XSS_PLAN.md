# XSS Fix Plan

## Changes

- `static/js/cineast.js` — Replaced `innerHTML` with `textContent` in `showToast` method.

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [x] All server-side template variables are autoescaped
- [x] Zero `|safe` filters applied to untrusted user input
- [x] Client-side DOM scripts use `textContent` rather than `innerHTML` for dynamic messages
- [x] Content Security Policy is active

## Manual verification (for the human)

- Create an entity or review with `<script>alert('XSS')</script>` in the name/content and verify that it is rendered strictly as text without executing.
