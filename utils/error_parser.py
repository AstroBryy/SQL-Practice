import re
import difflib

TABLE_NAMES = ["departments", "employees", "products", "customers", "orders", "order_items", "sales_reps"]

COLUMN_MAP = {
    "departments": ["id", "name", "location", "budget"],
    "employees": ["id", "first_name", "last_name", "dept_id", "salary", "hire_date", "manager_id", "is_active"],
    "products": ["id", "name", "category", "price", "stock_quantity"],
    "customers": ["id", "first_name", "last_name", "email", "city", "state", "registration_date"],
    "orders": ["id", "customer_id", "order_date", "status", "total_amount"],
    "order_items": ["id", "order_id", "product_id", "quantity", "unit_price"],
    "sales_reps": ["id", "employee_id", "region", "commission_rate", "ytd_sales"],
}

ALL_COLUMNS = [col for cols in COLUMN_MAP.values() for col in cols]


def explain_error(raw_error: str, error_type: str) -> dict:
    msg = raw_error.lower()

    if error_type == "forbidden":
        return {
            "title": "Query Not Allowed",
            "message": raw_error,
            "tip": "This environment is read-only. Only SELECT queries are permitted.",
            "suggestions": [],
        }

    if error_type == "timeout":
        return {
            "title": "Query Timed Out",
            "message": "Your query took too long to run.",
            "tip": "Add a LIMIT clause to reduce the result size, or check for unintended cartesian joins.",
            "suggestions": ["SELECT * FROM employees LIMIT 10"],
        }

    m = re.search(r'no such table: (\S+)', msg)
    if m:
        bad = m.group(1)
        close = difflib.get_close_matches(bad, TABLE_NAMES, n=2, cutoff=0.5)
        suggestions = [f"Did you mean: {c}?" for c in close]
        return {
            "title": "Table Not Found",
            "message": f"The table '{bad}' does not exist in this database.",
            "tip": f"Available tables: {', '.join(TABLE_NAMES)}",
            "suggestions": suggestions,
        }

    m = re.search(r'no such column: (\S+)', msg)
    if m:
        bad = m.group(1).split(".")[-1]
        close = difflib.get_close_matches(bad, ALL_COLUMNS, n=3, cutoff=0.4)
        suggestions = [f"Did you mean: {c}?" for c in close]
        found_in = [t for t, cols in COLUMN_MAP.items() if bad in cols]
        if found_in:
            suggestions.insert(0, f"'{bad}' exists in: {', '.join(found_in)}")
        return {
            "title": "Column Not Found",
            "message": f"The column '{bad}' does not exist.",
            "tip": "Check the Schema tab to see the exact column names for each table.",
            "suggestions": suggestions,
        }

    m = re.search(r"near [\"'](.+?)[\"']: syntax error", msg)
    if m:
        token = m.group(1)
        tips = {
            "from": "Check that your SELECT clause has the correct column names before FROM.",
            "where": "Make sure your JOIN clauses come before WHERE.",
            "select": "SELECT should be the very first keyword.",
            "group": "GROUP BY comes after WHERE. Check keyword order.",
            "order": "ORDER BY comes after GROUP BY (or WHERE if no GROUP BY).",
            "having": "HAVING comes after GROUP BY.",
            "limit": "LIMIT comes last, after ORDER BY.",
        }
        tip = tips.get(token.lower(), f"Check for a missing comma, keyword, or parenthesis near '{token}'.")
        return {
            "title": "Syntax Error",
            "message": f"There is a syntax error near '{token}'.",
            "tip": tip,
            "suggestions": ["Remember SQL clause order: SELECT → FROM → JOIN → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT"],
        }

    if "misuse of aggregate" in msg or "aggregate functions are not allowed" in msg:
        return {
            "title": "Aggregate Function Misuse",
            "message": "You used an aggregate function (COUNT, SUM, AVG, etc.) incorrectly.",
            "tip": "If you're aggregating along with other columns, you need a GROUP BY clause.",
            "suggestions": [
                "SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id",
                "SELECT COUNT(*) FROM employees  -- no GROUP BY needed if selecting ONLY aggregates",
            ],
        }

    if "ambiguous column name" in msg:
        m2 = re.search(r'ambiguous column name: (\S+)', msg)
        col = m2.group(1) if m2 else "a column"
        return {
            "title": "Ambiguous Column Name",
            "message": f"The column '{col}' exists in more than one table in your query.",
            "tip": "Use a table alias prefix, like e.id or o.id, to specify which table you mean.",
            "suggestions": [f"Replace '{col}' with 'tablealias.{col}'"],
        }

    if "no such function" in msg:
        m2 = re.search(r'no such function: (\S+)', msg)
        fn = m2.group(1) if m2 else "unknown"
        return {
            "title": "Unknown Function",
            "message": f"'{fn}' is not a recognized SQL function.",
            "tip": "SQLite supports functions like COUNT, SUM, AVG, MIN, MAX, LENGTH, UPPER, LOWER, SUBSTR, STRFTIME, COALESCE.",
            "suggestions": [],
        }

    return {
        "title": "SQL Error",
        "message": raw_error,
        "tip": "Check your query for typos, missing keywords, or incorrect syntax.",
        "suggestions": [],
    }


def explain_mismatch(reason: str, details: dict) -> dict:
    if reason == "column_mismatch":
        exp = details.get("expected", [])
        got = details.get("got", [])
        return {
            "title": "Wrong Columns",
            "message": f"Your query returned columns: {got}\nExpected columns: {exp}",
            "tip": "Make sure you SELECT the exact columns requested — check names, aliases, and order.",
            "suggestions": [],
        }
    if reason == "row_count_mismatch":
        exp = details.get("expected", "?")
        got = details.get("got", "?")
        direction = "too many rows" if got > exp else "too few rows"
        return {
            "title": "Wrong Number of Rows",
            "message": f"Your query returned {got} rows, but {exp} were expected.",
            "tip": f"You have {direction}. Check your WHERE / JOIN / HAVING conditions.",
            "suggestions": [],
        }
    if reason == "row_mismatch":
        return {
            "title": "Wrong Data",
            "message": "Your query returned the right number of rows and columns, but the values don't match.",
            "tip": "Check your filter values, JOIN conditions, and any calculations or CASE expressions.",
            "suggestions": [],
        }
    return {"title": "Incorrect", "message": "Your result did not match.", "tip": "", "suggestions": []}


def build_diff_tokens(user_sql: str, correct_sql: str) -> list:
    def tokenize(sql):
        parts = re.split(r'(\s+|,|\(|\)|=|<|>|\.|\*|;)', sql.strip())
        return [p for p in parts if p]

    user_tokens = tokenize(user_sql)
    correct_tokens = tokenize(correct_sql)

    sm = difflib.SequenceMatcher(None, user_tokens, correct_tokens)
    diff = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for t in user_tokens[i1:i2]:
                diff.append({"text": t, "status": "same"})
        elif tag == "replace":
            for t in user_tokens[i1:i2]:
                diff.append({"text": t, "status": "removed"})
            for t in correct_tokens[j1:j2]:
                diff.append({"text": t, "status": "added"})
        elif tag == "delete":
            for t in user_tokens[i1:i2]:
                diff.append({"text": t, "status": "removed"})
        elif tag == "insert":
            for t in correct_tokens[j1:j2]:
                diff.append({"text": t, "status": "added"})
    return diff
