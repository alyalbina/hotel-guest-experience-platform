import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.catalog import CATEGORIES, DEPARTMENTS, ROOMS


class Database:
    def __init__(self, path):
        self.path = Path(path)

    @contextmanager
    def connect(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA busy_timeout=10000")
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def initialize(self):
        with self.connect() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.executescript(Path(__file__).with_name("schema.sql").read_text())
            conn.executemany("INSERT OR IGNORE INTO departments VALUES (?,?,?)", DEPARTMENTS)
            conn.executemany("INSERT OR IGNORE INTO rooms VALUES (?)", [(r,) for r in ROOMS])
            conn.executemany("INSERT OR IGNORE INTO categories VALUES (?,?,?)", [c[:3] for c in CATEGORIES])
