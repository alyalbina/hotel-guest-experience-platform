import secrets
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from app.analytics import compute_metrics
from app.catalog import CATEGORIES
from app.config import Settings
from app.db import Database
from app.security import hash_password, token_hash, verify_password
from app.seed import seed_demo
from app.service import DomainError, Service, utcnow

STATIC = Path(__file__).parent / "static"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Login(StrictModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=200)


class Change(StrictModel):
    version: int = Field(ge=1)
    status: str | None = None
    assigned_to: int | None = None
    note: str = Field(default="", max_length=500)


class Create(StrictModel):
    guest_id: int = Field(ge=1)
    category: str
    service: str
    detail: str = Field(min_length=1, max_length=1000)


def create_app(settings=None):
    settings = settings or Settings.from_env()
    db, dummy_hash = Database(settings.database), hash_password("unusable-" + secrets.token_hex(24))
    service = Service(db)

    @asynccontextmanager
    async def lifespan(app):
        db.initialize()
        if settings.demo:
            seed_demo(db)
        yield

    app = FastAPI(
        title="Hotel Guest Experience Platform",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs" if settings.demo else None,
        redoc_url=None,
    )
    app.state.db, app.state.service = db, service

    @app.exception_handler(DomainError)
    async def domain_error(request, error):
        return JSONResponse({"detail": error.message}, status_code=error.status)

    @app.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        )
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    def current_staff(request: Request):
        token = request.cookies.get("hotel_session", "")
        with db.connect() as c:
            row = c.execute(
                """SELECT s.id,s.username,s.name,s.role,s.department_id,se.csrf
                FROM sessions se JOIN staff s ON s.id=se.staff_id WHERE token_hash=? AND expires_at>?""",
                (token_hash(token), utcnow()),
            ).fetchone()
        if not row:
            raise HTTPException(401, "Please sign in")
        if request.method not in {"GET", "HEAD", "OPTIONS"} and not secrets.compare_digest(
            request.headers.get("X-CSRF-Token", ""), row["csrf"]
        ):
            raise HTTPException(403, "Invalid CSRF token")
        return dict(row)

    @app.get("/")
    def index():
        return FileResponse(STATIC / "index.html")

    @app.get("/health")
    def health():
        with db.connect() as c:
            c.execute("SELECT 1").fetchone()
        return {"status": "ok", "demo": settings.demo}

    @app.get("/api/config")
    def configuration():
        return {
            "demo": settings.demo,
            "demo_username": "demo" if settings.demo else None,
            "demo_password": "PortfolioDemo2026!" if settings.demo else None,
        }

    @app.post("/api/login")
    def login(data: Login, request: Request, response: Response):
        now = datetime.now(timezone.utc)
        cutoff = (now - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
        client = token_hash(request.client.host if request.client else "unknown")
        with db.connect() as c:
            c.execute("DELETE FROM login_attempts WHERE occurred_at<?", (cutoff,))
            count = c.execute(
                "SELECT COUNT(*) FROM login_attempts WHERE client_hash=?", (client,)
            ).fetchone()[0]
            if count >= 10:
                raise HTTPException(429, "Too many sign-in attempts. Try in 15 minutes.")
            c.execute("INSERT INTO login_attempts VALUES (?,?)", (client, utcnow()))
        with db.connect() as c:
            user = c.execute("SELECT * FROM staff WHERE username=?", (data.username,)).fetchone()
            valid = verify_password(data.password, user["password_hash"] if user else dummy_hash)
            if not valid or not user:
                raise HTTPException(401, "Invalid username or password")
            token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
            c.execute("DELETE FROM sessions WHERE expires_at<=?", (utcnow(),))
            c.execute(
                "INSERT INTO sessions VALUES (?,?,?,?)",
                (
                    token_hash(token),
                    user["id"],
                    csrf,
                    (now + timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                ),
            )
        response.set_cookie(
            "hotel_session", token, httponly=True, secure=not settings.demo, samesite="strict", max_age=28800
        )
        return {"csrf": csrf, "name": user["name"], "role": user["role"]}

    @app.get("/api/me")
    def me(staff=Depends(current_staff)):
        return staff

    @app.post("/api/logout")
    def logout(request: Request, response: Response, staff=Depends(current_staff)):
        with db.connect() as c:
            c.execute(
                "DELETE FROM sessions WHERE token_hash=?",
                (token_hash(request.cookies.get("hotel_session", "")),),
            )
        response.delete_cookie("hotel_session")
        return {"ok": True}

    @app.get("/api/catalog")
    def catalog(staff=Depends(current_staff)):
        with db.connect() as c:
            departments = [dict(x) for x in c.execute("SELECT * FROM departments ORDER BY name")]
            employees = [
                dict(x) for x in c.execute("SELECT id,name,role,department_id FROM staff ORDER BY id")
            ]
            guests = (
                [dict(x) for x in c.execute("SELECT id,name,room_id FROM guests ORDER BY id")]
                if staff["role"] == "manager"
                else []
            )
        return {
            "departments": departments,
            "staff": employees,
            "guests": guests,
            "categories": [
                {"id": x[0], "name": x[1], "department": x[2], "services": x[3]} for x in CATEGORIES
            ],
        }

    def filter_dates(start, end):
        try:
            if start:
                date.fromisoformat(start)
            if end:
                date.fromisoformat(end)
            if start and end and start > end:
                raise ValueError
        except ValueError:
            raise HTTPException(422, "Use YYYY-MM-DD dates; start must not follow end") from None

    @app.get("/api/requests")
    def requests(
        status: str | None = None,
        department: str | None = None,
        search: str = "",
        start: str | None = None,
        end: str | None = None,
        staff=Depends(current_staff),
    ):
        filter_dates(start, end)
        return service.list_requests(staff, status, department, search[:100], start, end)

    @app.get("/api/requests/{request_id}")
    def detail(request_id: str, staff=Depends(current_staff)):
        return service.detail(request_id, staff)

    @app.patch("/api/requests/{request_id}")
    def change(request_id: str, data: Change, staff=Depends(current_staff)):
        assign = "assigned_to" in data.model_fields_set
        if data.status and assign:
            raise HTTPException(422, "Choose one action per update")
        return service.mutate(
            request_id, staff, data.version, data.status, data.assigned_to, data.note, assign
        )

    @app.post("/api/requests", status_code=201)
    def create(data: Create, staff=Depends(current_staff)):
        if staff["role"] != "manager":
            raise HTTPException(403, "Only managers can create requests for guests")
        rid = service.create_request(data.guest_id, data.category, data.service, data.detail)
        return service.detail(rid, staff)

    @app.get("/api/metrics")
    def metrics(
        department: str | None = None,
        start: str | None = None,
        end: str | None = None,
        staff=Depends(current_staff),
    ):
        filter_dates(start, end)
        return {
            "demo": settings.demo,
            **compute_metrics(service.list_requests(staff, department=department, start=start, end=end)),
        }

    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app
