import sqlite3
from pathlib import Path
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# keep db and schema paths relative to this file
BASE_DIR = Path(__file__).resolve().parent
DB = str(BASE_DIR / "tracker.db")


def db():
    # open a sqlite connection and return rows like dicts
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # create tables if they do not exist
    conn = db()
    cur = conn.cursor()

    schema_path = BASE_DIR / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

    conn.commit()
    conn.close()


def parse_week_param(week_str):
    # week_str should look like "YYYY-MM-DD"
    chosen = date.today()
    if week_str:
        try:
            chosen = datetime.strptime(week_str, "%Y-%m-%d").date()
        except ValueError:
            chosen = date.today()

    # normalize to monday
    monday = chosen - timedelta(days=chosen.weekday())
    return monday


def build_week(monday):
    # build 7 days starting from monday
    today = date.today()
    week = []
    for i in range(7):
        d = monday + timedelta(days=i)
        week.append({
            "label": d.strftime("%a %b %d"),
            "iso": d.isoformat(),
            "is_today": (d == today)
        })
    return week


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/system")
def system():
    return render_template("system.html")


@app.route("/habits", methods=["GET", "POST"])
def habits():
    conn = db()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        habit_type = request.form.get("type", "").strip()

        if name != "" and habit_type in ("start", "cut"):
            cur.execute(
                "INSERT INTO habits (name, type) VALUES (?, ?)",
                (name, habit_type)
            )
            conn.commit()

        conn.close()
        return redirect("/habits")

    habit_rows = cur.execute(
        "SELECT id, name, type FROM habits ORDER BY id DESC"
    ).fetchall()

    conn.close()
    return render_template("habits.html", habits=habit_rows)


@app.route("/table")
def table():
    week_param = request.args.get("week", "")
    monday = parse_week_param(week_param)
    week = build_week(monday)

    start_iso = week[0]["iso"]
    end_iso = week[-1]["iso"]

    prev_monday = (monday - timedelta(days=7)).isoformat()
    next_monday = (monday + timedelta(days=7)).isoformat()
    this_monday = (date.today() - timedelta(days=date.today().weekday())).isoformat()

    conn = db()
    cur = conn.cursor()

    habits = cur.execute(
        "SELECT id, name, type FROM habits ORDER BY id"
    ).fetchall()

    # only load checks for the selected week
    check_rows = cur.execute(
        """
        SELECT habit_id, check_date, done
        FROM checks
        WHERE check_date >= ? AND check_date <= ?
        """,
        (start_iso, end_iso)
    ).fetchall()

    done = {}
    for r in check_rows:
        done[(r["habit_id"], r["check_date"])] = (r["done"] == 1)

    conn.close()

    return render_template(
        "table.html",
        habits=habits,
        week=week,
        done=done,
        week_start=monday.isoformat(),
        prev_week=prev_monday,
        next_week=next_monday,
        this_week=this_monday
    )


@app.route("/toggle", methods=["POST"])
def toggle():
    habit_id = int(request.form["habit_id"])
    check_date = request.form["check_date"]
    week_start = request.form.get("week_start", "")

    conn = db()
    cur = conn.cursor()

    row = cur.execute(
        "SELECT done FROM checks WHERE habit_id=? AND check_date=?",
        (habit_id, check_date)
    ).fetchone()

    if row is None:
        cur.execute(
            "INSERT INTO checks (habit_id, check_date, done) VALUES (?, ?, 1)",
            (habit_id, check_date)
        )
    else:
        new_done = 0 if row["done"] == 1 else 1
        cur.execute(
            "UPDATE checks SET done=? WHERE habit_id=? AND check_date=?",
            (new_done, habit_id, check_date)
        )

    conn.commit()
    conn.close()

    # go back to the same week view
    if week_start:
        return redirect(url_for("table", week=week_start))
    return redirect("/table")


@app.route("/habits/delete", methods=["POST"])
def delete_habit():
    habit_id = int(request.form["habit_id"])

    conn = db()
    cur = conn.cursor()

    # delete checks first
    cur.execute("DELETE FROM checks WHERE habit_id = ?", (habit_id,))
    cur.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

    conn.commit()
    conn.close()

    return redirect("/habits")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
