# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Spendly" — a Flask expense-tracker **teaching skeleton**. The app is intentionally
incomplete: it ships working public pages (landing, login, register, terms, privacy)
plus a set of stubbed routes and an empty database module that a student fills in
step by step. When working here, respect that structure — don't implement the
student steps unless explicitly asked, and match the "Step N" framing already in the code.

## Commands

The virtualenv lives in `venv/`. Activate it first (PowerShell): `venv\Scripts\Activate.ps1`.

- Install deps: `pip install -r requirements.txt`
- Run the dev server: `python app.py` — serves on **http://127.0.0.1:5001** with `debug=True`
- Run tests: `pytest`
- Run a single test: `pytest path/to/test_file.py::test_name`

There are no test files yet; `pytest` + `pytest-flask` are installed for the student steps.

## Architecture

- `app.py` — the entire Flask app: route definitions only, no app factory. Public routes
  call `render_template(...)`; unimplemented features are placeholder routes that return a
  literal `"... — coming in Step N"` string. These are the seams students replace.
- `database/db.py` — **empty placeholder** (a docstring spec only). It is meant to expose
  `get_db()` (SQLite connection with `row_factory` + foreign keys on), `init_db()`
  (`CREATE TABLE IF NOT EXISTS`), and `seed_db()`. The DB file `expense_tracker.db` is
  gitignored and created at runtime once `db.py` is implemented.
- `templates/` — Jinja2. `base.html` defines the shell (navbar, footer, `style.css`,
  `main.js`) and the `title`/`head`/`content`/`scripts` blocks; all pages extend it.
- `static/css/` — `style.css` is the global stylesheet loaded by `base.html`;
  `landing.css` is landing-page-specific. `static/js/main.js` is the shared script.

## Conventions

- Brand name is **Spendly**; the diamond glyph `◈` is the logo. Tagline: "Track every rupee."
  (currency context is INR).
- Fonts are loaded from Google Fonts in `base.html` (DM Serif Display + DM Sans).
- Reference routes by their `url_for` endpoint name (`landing`, `login`, `register`,
  `terms`, `privacy`), matching the existing templates.

## Repo notes

- `CLAUDE_SUMMARY.md`, `file.md`, `file.txt`, and `Screenshot*.png` are gitignored local
  scratch/learning files, not part of the app. `CLAUDE_SUMMARY.md` is a personal Claude Code
  learning log — when the user says "generate summary", append new learnings to it.
