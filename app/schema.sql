PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS departments (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, sla_minutes INTEGER NOT NULL CHECK(sla_minutes>0)
);
CREATE TABLE IF NOT EXISTS rooms (id TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS categories (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, department_id TEXT NOT NULL REFERENCES departments(id)
);
CREATE TABLE IF NOT EXISTS staff (
  id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('manager','agent','analyst')),
  department_id TEXT REFERENCES departments(id), password_hash TEXT NOT NULL,
  CHECK(role != 'agent' OR department_id IS NOT NULL)
);
CREATE TABLE IF NOT EXISTS guests (
  id INTEGER PRIMARY KEY, telegram_id INTEGER UNIQUE,
  name TEXT NOT NULL, room_id TEXT NOT NULL REFERENCES rooms(id),
  birthday TEXT, gender TEXT, email TEXT, phone TEXT, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS requests (
  id TEXT PRIMARY KEY, guest_id INTEGER NOT NULL REFERENCES guests(id),
  category_id TEXT NOT NULL REFERENCES categories(id),
  department_id TEXT NOT NULL REFERENCES departments(id),
  service TEXT NOT NULL, detail TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('new','acknowledged','in_progress','resolved','reopened','cancelled')),
  assigned_to INTEGER REFERENCES staff(id), created_at TEXT NOT NULL,
  responded_at TEXT, first_resolved_at TEXT, resolved_at TEXT,
  sla_minutes INTEGER NOT NULL CHECK(sla_minutes>0),
  reopen_count INTEGER NOT NULL DEFAULT 0 CHECK(reopen_count>=0),
  csat INTEGER CHECK(csat BETWEEN 1 AND 5), version INTEGER NOT NULL DEFAULT 1,
  source_ref TEXT UNIQUE,
  CHECK(responded_at IS NULL OR responded_at >= created_at),
  CHECK(resolved_at IS NULL OR resolved_at >= created_at)
);
CREATE TABLE IF NOT EXISTS request_events (
  id INTEGER PRIMARY KEY, request_id TEXT NOT NULL REFERENCES requests(id),
  actor_id INTEGER REFERENCES staff(id), action TEXT NOT NULL,
  from_status TEXT, to_status TEXT, note TEXT NOT NULL DEFAULT '', occurred_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions (
  token_hash TEXT PRIMARY KEY, staff_id INTEGER NOT NULL REFERENCES staff(id),
  csrf TEXT NOT NULL, expires_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS login_attempts (client_hash TEXT NOT NULL, occurred_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS idx_request_queue ON requests(department_id,status,created_at);
CREATE INDEX IF NOT EXISTS idx_events_request ON request_events(request_id,occurred_at);
CREATE INDEX IF NOT EXISTS idx_attempts ON login_attempts(client_hash,occurred_at);
CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY);
INSERT OR IGNORE INTO schema_version VALUES (1);
