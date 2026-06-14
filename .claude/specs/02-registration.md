# Spec: Registration

## Overview

Turn the existing `/register` page into a working sign-up flow. Today the
`register` route only renders `register.html` (a GET-only stub) and the form's
POST goes nowhere. This step makes `/register` accept the submitted form,
validate the input, create a new row in the `users` table with a securely
hashed password, and send the new user on to the login page. It is the first
write-path feature in Spendly and the foundation for authentication (Step 3,
login/logout) and every per-user feature after it.

## Depends on

- **Step 1 — Database setup** (complete): `database/db.py` provides `get_db()`,
  `init_db()`, `seed_db()` and the `users` table (`id`, `name`, `email`,
  `password_hash`, `created_at`) with a `UNIQUE` constraint on `email`.

## Routes

- `GET /register` — render the registration form (existing behaviour, unchanged) — public
- `POST /register` — validate input, create the user, redirect to login on success; re-render the form with an error message on failure — public

The two are served by the same `register` view function in `app.py` (add
`methods=["GET", "POST"]`). No other routes change.

## Database changes

No database changes. The `users` table from Step 1 already has every column
this feature needs, including the `UNIQUE` constraint on `email`.

## Templates

- **Create:** none.
- **Modify:** none required. `templates/register.html` already extends
  `base.html`, posts to `/register`, sends `name` / `email` / `password`
  fields, and renders an `{{ error }}` block. The route should reuse that
  existing `error` variable for validation messages.

## Files to change

- `app.py` — change the `register` view to handle `GET` and `POST`: read the
  form fields, validate, insert the new user via `get_db()`, and
  `redirect(url_for("login"))` on success. Add the required imports
  (`request`, `redirect`, `url_for`).

## Files to create

- None.

## New dependencies

No new dependencies. Uses `werkzeug.security.generate_password_hash` (already a
project dependency) and the standard-library `sqlite3` via `database/db.py`.

## Rules for implementation

- No SQLAlchemy or ORMs — use `get_db()` from `database/db.py`.
- Parameterised queries only — never build SQL with string formatting / f-strings.
- Hash passwords with `werkzeug.security.generate_password_hash`; never store
  the plaintext password.
- Use CSS variables — never hardcode hex values. (No template/CSS changes are
  expected here, but follow this if any are added.)
- All templates extend `base.html`.
- Strip and validate input server-side: require `name`, a non-empty `email`,
  and a `password` of at least 8 characters; do not trust client-side `required`
  attributes alone.
- Normalise email before storing/checking (e.g. `strip()` and lowercase) so the
  `UNIQUE` constraint behaves predictably.
- Handle the duplicate-email case gracefully: either pre-check with a `SELECT`
  or catch `sqlite3.IntegrityError`, and re-render the form with a clear error
  rather than returning a 500.
- Close the database connection (the existing `db.py` connections are not
  context-managed for you).
- On success, redirect to the login page (`url_for("login")`) — do not log the
  user in (sessions arrive in Step 3).

## Definition of done

- [ ] `GET /register` still renders the form exactly as before.
- [ ] Submitting valid details creates exactly one new row in `users` with a
      hashed `password_hash` (not plaintext) and redirects to `/login`.
- [ ] Submitting an email that already exists re-renders the form with a visible
      error and does **not** create a duplicate row (no 500 error).
- [ ] Submitting a password shorter than 8 characters re-renders the form with a
      visible error and creates no row.
- [ ] Submitting with a missing/blank `name`, `email`, or `password` re-renders
      the form with a visible error and creates no row.
- [ ] No plaintext passwords are ever written to the database.
- [ ] The app still starts with `python app.py` and serves on
      http://127.0.0.1:5001 without errors.
