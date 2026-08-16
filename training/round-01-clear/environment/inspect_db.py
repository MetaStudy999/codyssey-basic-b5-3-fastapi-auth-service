import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "reference" / "database.db"

if not DB_PATH.exists():
    raise SystemExit(f"[FAIL] database not found: {DB_PATH}")

with sqlite3.connect(DB_PATH) as connection:
    users = connection.execute("SELECT id, username FROM users ORDER BY id").fetchall()
    projects = connection.execute("SELECT id, name, owner_id FROM projects ORDER BY id").fetchall()
    tasks = connection.execute(
        "SELECT id, title, is_done, project_id FROM tasks ORDER BY id"
    ).fetchall()

print(f"[PASS] database: {DB_PATH}")
print(f"[PASS] users={len(users)} projects={len(projects)} tasks={len(tasks)}")
print("users:", users)
print("projects:", projects)
print("tasks:", tasks)
