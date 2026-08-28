# SQL_INJECTION Fix Plan

## Changes

- None required (All queries are 100% parameterized via Django ORM).

## New files

- None

## Verification goals

After implementation, ALL of these must be true:

- [x] Every database interaction uses Django ORM querysets
- [x] Grep for `.raw(`, `.extra(`, and `cursor.execute` returns zero unsafe matches in application code
- [x] All user inputs are safely escaped and parameterized

## Manual verification (for the human)

- Test searching for SQL injection test strings (e.g. `' OR '1'='1`) in the search bar and verify that the query is treated as literal search text without error.
