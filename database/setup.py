import os
import sqlite3
from .schema import TABLES
from .seed import seed_database

DB_PATH = os.path.join(os.path.dirname(__file__), "practice.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def build_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for ddl in TABLES:
        cur.execute(ddl)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM employees")
    count = cur.fetchone()[0]
    if count == 0:
        seed_database(conn)
    conn.close()


def get_table_schemas():
    conn = get_connection()
    schemas = {}
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    for tbl in tables:
        cur.execute(f"PRAGMA table_info({tbl})")
        cols = [{"name": r[1], "type": r[2], "notnull": bool(r[3]), "pk": bool(r[5])} for r in cur.fetchall()]
        cur.execute(f"SELECT COUNT(*) FROM {tbl}")
        row_count = cur.fetchone()[0]
        schemas[tbl] = {"columns": cols, "row_count": row_count}
    conn.close()
    return schemas


def get_sample_rows(table, limit=5):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} LIMIT {limit}")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
