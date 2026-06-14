"""SQLite data layer for Spendly (Step 1 — Database Setup).

Exposes:
    get_db()   — SQLite connection with row_factory + foreign keys enabled
    init_db()  — creates all tables using CREATE TABLE IF NOT EXISTS
    seed_db()  — inserts demo data once for development
"""

import os
import sqlite3
from datetime import datetime

from werkzeug.security import generate_password_hash

# DB file lives in the project root, regardless of the current working dir.
# os.path.dirname(__file__) -> database/  ; one level up -> project root.
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "expense_tracker.db",
)

# Fixed category list (see spec section 10).
CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
]


def get_db():
    """Return a SQLite connection.

    sqlite3.connect() creates the DB file if it does not exist yet, so the
    database is created on first use (i.e. on startup via init_db()).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # dict-like row access
    conn.execute("PRAGMA foreign_keys = ON")  # enforce FKs on every connection
    return conn


def init_db():
    """Create both tables. Safe to call repeatedly (CREATE TABLE IF NOT EXISTS)."""
    conn = get_db()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                email         TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at    TEXT DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                amount      REAL NOT NULL,
                category    TEXT NOT NULL,
                date        TEXT NOT NULL,
                description TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def seed_db():
    """Insert one demo user and 8 sample expenses, only if the DB is empty."""
    conn = get_db()
    try:
        # Bail out if data already exists — prevents duplicate seeds.
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count > 0:
            return

        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
        )
        user_id = cursor.lastrowid

        # Dates spread across the current month, YYYY-MM-DD format.
        now = datetime.now()

        def day(d):
            return f"{now.year:04d}-{now.month:02d}-{d:02d}"

        # 8 expenses covering all 7 categories (Food appears twice).
        expenses = [
            (user_id, 250.0, "Food", day(2), "Lunch with colleagues"),
            (user_id, 60.0, "Transport", day(4), "Auto rickshaw fare"),
            (user_id, 1499.0, "Bills", day(5), "Electricity bill"),
            (user_id, 800.0, "Health", day(7), "Pharmacy — medicines"),
            (user_id, 499.0, "Entertainment", day(9), "Movie tickets"),
            (user_id, 2199.0, "Shopping", day(11), "New running shoes"),
            (user_id, 150.0, "Other", day(12), "Misc household items"),
            (user_id, 180.0, "Food", day(13), "Groceries"),
        ]
        conn.executemany(
            """
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            expenses,
        )
        conn.commit()
    finally:
        conn.close()
