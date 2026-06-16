import re
import sqlite3
import threading
from dataclasses import dataclass, field
from database.setup import DB_PATH

MAX_ROWS = 500
TIMEOUT_SECONDS = 5

FORBIDDEN_RE = re.compile(
    r'\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|GRANT|REVOKE|ATTACH|DETACH|PRAGMA|VACUUM|REPLACE)\b',
    re.IGNORECASE,
)

MULTI_STMT_RE = re.compile(r';\s*\S')


@dataclass
class QueryResult:
    ok: bool
    columns: list = field(default_factory=list)
    rows: list = field(default_factory=list)
    truncated: bool = False
    error_type: str = None
    raw_error: str = None


def _safe_authorizer(action, arg1, arg2, db_name, trigger_name):
    ALLOWED = {20, 21, 31, 34}  # READ, SELECT, FUNCTION, RECURSIVE
    return 0 if action in ALLOWED else 1  # 0=ok, 1=deny


def run_query(sql: str) -> QueryResult:
    sql = sql.strip()

    if FORBIDDEN_RE.search(sql):
        return QueryResult(ok=False, error_type="forbidden",
                           raw_error="Only SELECT queries are allowed in this practice environment.")

    if MULTI_STMT_RE.search(sql):
        return QueryResult(ok=False, error_type="forbidden",
                           raw_error="Multiple statements are not allowed. Write one SELECT query at a time.")

    result_holder = {}

    def _execute():
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.set_authorizer(_safe_authorizer)
            conn.row_factory = sqlite3.Row
            cur = conn.execute(sql)
            all_rows = cur.fetchmany(MAX_ROWS + 1)
            truncated = len(all_rows) > MAX_ROWS
            rows = [tuple(r) for r in all_rows[:MAX_ROWS]]
            columns = [d[0] for d in cur.description] if cur.description else []
            conn.close()
            result_holder["result"] = QueryResult(ok=True, columns=columns, rows=rows, truncated=truncated)
        except sqlite3.Error as e:
            result_holder["result"] = QueryResult(ok=False, error_type="sql_error", raw_error=str(e))
        except Exception as e:
            result_holder["result"] = QueryResult(ok=False, error_type="unknown", raw_error=str(e))

    t = threading.Thread(target=_execute, daemon=True)
    t.start()
    t.join(timeout=TIMEOUT_SECONDS)

    if t.is_alive():
        return QueryResult(ok=False, error_type="timeout",
                           raw_error="Your query took too long. Try adding a LIMIT clause.")

    return result_holder.get("result", QueryResult(ok=False, error_type="unknown", raw_error="Unknown error."))


def normalize_rows(rows):
    normalized = []
    for row in rows:
        norm_row = []
        for val in row:
            if val is None:
                norm_row.append("NULL")
            elif isinstance(val, float):
                norm_row.append(str(round(val, 2)))
            else:
                norm_row.append(str(val).strip())
        normalized.append(tuple(norm_row))
    return normalized


def compare_results(user_result: QueryResult, expected_result: QueryResult,
                    order_sensitive=False, allow_extra_columns=False):
    if not user_result.ok:
        return {"match": False, "reason": "user_error"}
    if not expected_result.ok:
        return {"match": False, "reason": "solution_error"}

    u_cols = [c.lower() for c in user_result.columns]
    e_cols = [c.lower() for c in expected_result.columns]

    if not allow_extra_columns and u_cols != e_cols:
        return {
            "match": False,
            "reason": "column_mismatch",
            "details": {"expected": e_cols, "got": u_cols},
        }

    u_rows = normalize_rows(user_result.rows)
    e_rows = normalize_rows(expected_result.rows)

    if not order_sensitive:
        u_rows = sorted(u_rows)
        e_rows = sorted(e_rows)

    if len(u_rows) != len(e_rows):
        return {
            "match": False,
            "reason": "row_count_mismatch",
            "details": {"expected": len(e_rows), "got": len(u_rows)},
        }

    if u_rows != e_rows:
        return {"match": False, "reason": "row_mismatch"}

    return {"match": True, "reason": "ok"}
