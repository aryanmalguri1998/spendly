import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)

# Signs the session cookie. Override in production via the SECRET_KEY env var.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# Ensure the database file, schema, and demo data are ready before any request.
with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not name or not email or not password:
            return render_template("register.html",
                                   error="All fields are required.")
        if len(password) < 8:
            return render_template("register.html",
                                   error="Password must be at least 8 characters.")

        conn = get_db()
        try:
            existing = conn.execute(
                "SELECT id FROM users WHERE email = ?", (email,)
            ).fetchone()
            if existing:
                return render_template("register.html",
                                       error="An account with that email already exists.")
            conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, generate_password_hash(password)),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template("register.html",
                                   error="An account with that email already exists.")
        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        # One generic message for every failure — never reveal whether the
        # email exists or the password was wrong (no account enumeration).
        error = "Invalid email or password."

        if not email or not password:
            return render_template("login.html", error=error)

        conn = get_db()
        try:
            user = conn.execute(
                "SELECT id, name, password_hash FROM users WHERE email = ?",
                (email,),
            ).fetchone()
        finally:
            conn.close()

        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error=error)

        session.clear()
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("landing"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    # Logged-in only — bounce anonymous visitors to the sign-in page.
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Step 4 is UI-only: every value below is hardcoded. Step 5 swaps this
    # block for real queries against the users/expenses tables via get_db().
    user = {
        "name": session.get("user_name", "Demo User"),
        "email": "demo@spendly.com",
        "initials": "DU",
        "member_since": "January 2026",
    }

    stats = [
        {"label": "Total spent", "value": "₹48,250"},
        {"label": "Transactions", "value": "24"},
        {"label": "Top category", "value": "Food & Dining"},
    ]

    transactions = [
        {"date": "12 Jun 2026", "description": "Grocery run — DMart",
         "category": "Groceries", "slug": "groceries", "amount": "₹2,340"},
        {"date": "10 Jun 2026", "description": "Dinner at Truffles",
         "category": "Food & Dining", "slug": "food", "amount": "₹1,180"},
        {"date": "08 Jun 2026", "description": "Metro card recharge",
         "category": "Transport", "slug": "transport", "amount": "₹500"},
        {"date": "05 Jun 2026", "description": "Netflix subscription",
         "category": "Entertainment", "slug": "entertainment", "amount": "₹649"},
        {"date": "02 Jun 2026", "description": "Electricity bill",
         "category": "Utilities", "slug": "utilities", "amount": "₹1,890"},
    ]

    categories = [
        {"name": "Food & Dining", "slug": "food", "amount": "₹18,400", "percent": 38},
        {"name": "Groceries", "slug": "groceries", "amount": "₹12,100", "percent": 25},
        {"name": "Transport", "slug": "transport", "amount": "₹7,250", "percent": 15},
        {"name": "Utilities", "slug": "utilities", "amount": "₹6,300", "percent": 13},
        {"name": "Entertainment", "slug": "entertainment", "amount": "₹4,200", "percent": 9},
    ]

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
