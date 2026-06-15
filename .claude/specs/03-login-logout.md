# Spec: Login and Logout

## Overview

Give Spendly real authentication. Today `/login` is a GET-only stub that just
renders `login.html` (its form POSTs nowhere) and `/logout` is a placeholder
string ("Logout — coming in Step 3"). This step turns `/login` into a working
sign-in flow that verifies a submitted email/password against the hashed
credentials in the `users` table and, on success, records the user in a Flask
`session`. `/logout` clears that session. This is the first feature to use
sessions and is the gate every per-user feature after it (profile, expenses)
will sit behind.

## Depends on

- **Step 1 — Database setup** (complete): `database/db.py` provides `get_db()`
  and the `users` table (`id`, `name`, `email`, `password_hash`, `created_at`).
- **Step 2 — Registration** (complete): `/register` writes new users with a
  `werkzeug`-hashed `password_hash`, so there are real accounts to sign in with.
  The seeded `demo@spendly.com` / `demo123` account also works.

## Routes

- `GET /login` — render the sign-in form (existing behaviour, unchanged) — public
- `POST /login` — validate credentials, set the session, redirect on success;
  re-render the form with an error on failure — public
- `GET /logout` — clear the session and redirect to `/login` — logged-in
  (harmless if called while logged out)

`GET` and `POST /login` are served by the same `login` view in `app.py` (add
`methods=["GET", "POST"]`). The existing `logout` placeholder view is replaced.

## Database changes

No database changes. The `users` table from Step 1 already stores the
`email` and `password_hash` needed to authenticate.

## Templates

- **Create:** none.
- **Modify:**
  - `templates/login.html` — no structural change required. It already extends
    `base.html`, POSTs `email` / `password`, and renders an `{{ error }}` block;
    the route reuses that `error` variable for the "invalid credentials" message.
  - `templates/base.html` — make the navbar auth-aware so logout is reachable
    from the UI: when `session.user_id` is set, show a "Sign out"
    (`url_for('logout')`) link instead of the "Sign in" / "Get started" links.

## Files to change

- `app.py`
  - Set `app.secret_key` so Flask can sign the session cookie.
  - Import `session` from `flask` and `check_password_hash` from
    `werkzeug.security`.
  - Change the `login` view to handle `GET` and `POST`: read and normalise the
    form fields, look up the user by email, verify the password with
    `check_password_hash`, store `user_id` (and optionally `user_name`) in the
    session, and redirect on success; re-render `login.html` with an `error` on
    failure.
  - Replace the `logout` placeholder with a view that calls `session.clear()`
    and redirects to `url_for("login")`.
- `templates/base.html` — conditional navbar links (see Templates).

## Files to create

- None.

## New dependencies

No new dependencies. Sessions use Flask's built-in `session`; password
verification uses `werkzeug.security.check_password_hash` (already installed).

## Rules for implementation

- No SQLAlchemy or ORMs — use `get_db()` from `database/db.py`.
- Parameterised queries only — never build SQL with string formatting / f-strings.
- Passwords are verified with `werkzeug.security.check_password_hash` against the
  stored `password_hash`; never compare plaintext and never log the password.
- Set `app.secret_key` from an environment variable (e.g.
  `os.environ.get("SECRET_KEY", "<dev-fallback>")`) so the dev default is
  overridable; the session cookie is unsigned/insecure without it.
- Normalise the submitted email the same way registration does (`strip()` +
  lowercase) so lookups match stored rows.
- Use a single generic error message ("Invalid email or password.") for both an
  unknown email and a wrong password — do not reveal which one was wrong.
- Validate server-side that `email` and `password` are present; do not trust the
  client-side `required` attributes alone.
- Close the database connection (the `db.py` connections are not
  context-managed for you).
- Use CSS variables — never hardcode hex values (applies to any
  navbar/template tweak).
- All templates extend `base.html`.

## Definition of done

- [ ] `GET /login` still renders the form exactly as before.
- [ ] Signing in with `demo@spendly.com` / `demo123` (or any registered account)
      sets the session and redirects to a logged-in destination, not back to the
      login form.
- [ ] A wrong password re-renders the form with a visible generic error and does
      **not** set the session.
- [ ] An unrecognised email re-renders the form with the **same** generic error
      (no account-enumeration leak) and does not set the session.
- [ ] Submitting with a blank `email` or `password` re-renders the form with a
      visible error.
- [ ] While logged in, the navbar shows a "Sign out" link; clicking it hits
      `/logout`, clears the session, and returns to `/login`.
- [ ] Visiting `/logout` while already logged out redirects to `/login` without
      error.
- [ ] The app still starts with `python app.py` and serves on
      http://127.0.0.1:5001 without errors.
