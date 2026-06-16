import os
import json
from flask import Flask, render_template, request, jsonify, session
from database.setup import build_database, get_table_schemas, get_sample_rows
from utils.sql_runner import run_query, compare_results
from utils.error_parser import explain_error, explain_mismatch, build_diff_tokens
from challenges import get_challenge, list_challenges, ALL_CHALLENGES
from lessons import get_lesson, list_lessons

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-sql-practice-42")


@app.before_request
def ensure_db():
    if not hasattr(app, "_db_ready"):
        build_database()
        app._db_ready = True


# ── Page Routes ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    stats = {
        "beginner": len(list_challenges("beginner")),
        "intermediate": len(list_challenges("intermediate")),
        "advanced": len(list_challenges("advanced")),
        "analyst": len(list_challenges(category="Random Analyst")),
    }
    return render_template("index.html", stats=stats)


@app.route("/practice")
@app.route("/practice/<difficulty>")
def practice(difficulty=None):
    if difficulty and difficulty not in ("beginner", "intermediate", "advanced", "analyst"):
        difficulty = None
    if difficulty == "analyst":
        challenges = list_challenges(category="Random Analyst")
    elif difficulty:
        challenges = list_challenges(difficulty)
    else:
        challenges = list(ALL_CHALLENGES.values())
    categories = {}
    for c in challenges:
        cat = c["category"]
        categories.setdefault(cat, []).append(c)
    return render_template("practice.html", challenges=challenges, categories=categories,
                           difficulty=difficulty)


@app.route("/challenge/<challenge_id>")
def challenge(challenge_id):
    ch = get_challenge(challenge_id)
    if not ch:
        return render_template("404.html"), 404
    sample_data = {}
    for tbl in ch.get("tables", []):
        sample_data[tbl] = get_sample_rows(tbl, 5)
    return render_template("challenge.html", challenge=ch, sample_data=sample_data)


@app.route("/learn")
@app.route("/learn/<difficulty>")
def learn(difficulty=None):
    if difficulty and difficulty not in ("beginner", "intermediate", "advanced"):
        difficulty = None
    if difficulty:
        lessons = list_lessons(difficulty)
    else:
        lessons = list_lessons()
    return render_template("lessons.html", lessons=lessons, difficulty=difficulty)


@app.route("/lesson/<lesson_id>")
def lesson(lesson_id):
    l = get_lesson(lesson_id)
    if not l:
        return render_template("404.html"), 404
    try_challenge = None
    if l.get("try_challenge_id"):
        try_challenge = get_challenge(l["try_challenge_id"])
    return render_template("lesson_detail.html", lesson=l, try_challenge=try_challenge)


@app.route("/schema")
def schema():
    schemas = get_table_schemas()
    samples = {tbl: get_sample_rows(tbl, 5) for tbl in schemas}
    return render_template("schema.html", schemas=schemas, samples=samples)


# ── API Routes ────────────────────────────────────────────────────────────────

@app.route("/api/run", methods=["POST"])
def api_run():
    data = request.get_json(silent=True) or {}
    sql = data.get("sql", "").strip()
    if not sql:
        return jsonify({"ok": False, "error": {"title": "Empty Query", "message": "Please enter a SQL query.", "tip": "", "suggestions": []}}), 400

    result = run_query(sql)
    if not result.ok:
        error_info = explain_error(result.raw_error or "", result.error_type or "unknown")
        return jsonify({"ok": False, "error": error_info})

    return jsonify({
        "ok": True,
        "columns": result.columns,
        "rows": result.rows,
        "truncated": result.truncated,
        "row_count": len(result.rows),
    })


@app.route("/api/check/<challenge_id>", methods=["POST"])
def api_check(challenge_id):
    ch = get_challenge(challenge_id)
    if not ch:
        return jsonify({"ok": False, "error": {"title": "Not Found", "message": "Challenge not found.", "tip": "", "suggestions": []}}), 404

    data = request.get_json(silent=True) or {}
    user_sql = data.get("sql", "").strip()
    if not user_sql:
        return jsonify({"ok": False, "error": {"title": "Empty Query", "message": "Please enter a SQL query.", "tip": "", "suggestions": []}}), 400

    user_result = run_query(user_sql)
    if not user_result.ok:
        error_info = explain_error(user_result.raw_error or "", user_result.error_type or "unknown")
        return jsonify({"status": "error", "error": error_info, "diff": None})

    solution_result = run_query(ch["solution_sql"])
    validation = ch.get("validation", {})
    comparison = compare_results(
        user_result, solution_result,
        order_sensitive=validation.get("order_sensitive", False),
        allow_extra_columns=validation.get("allow_extra_columns", False),
    )

    if comparison["match"]:
        progress = session.get("completed", [])
        if challenge_id not in progress:
            progress.append(challenge_id)
            session["completed"] = progress
        return jsonify({
            "status": "correct",
            "columns": user_result.columns,
            "rows": user_result.rows,
            "row_count": len(user_result.rows),
            "message": "Correct! Well done.",
        })
    else:
        mismatch_info = explain_mismatch(comparison["reason"], comparison.get("details", {}))
        diff = build_diff_tokens(user_sql, ch["solution_sql"])
        return jsonify({
            "status": "incorrect",
            "error": mismatch_info,
            "diff": diff,
            "solution_sql": ch["solution_sql"],
            "columns": user_result.columns,
            "rows": user_result.rows,
            "row_count": len(user_result.rows),
        })


@app.route("/api/schema")
def api_schema():
    return jsonify(get_table_schemas())


@app.route("/api/progress")
def api_progress():
    completed = session.get("completed", [])
    return jsonify({
        "completed": completed,
        "total": len(ALL_CHALLENGES),
        "count": len(completed),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
