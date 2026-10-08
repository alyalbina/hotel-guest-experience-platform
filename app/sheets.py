"""Optional explicit request snapshot export, never on the guest submission path."""

from app.service import Service

HEADERS = [
    "request_id",
    "department",
    "category",
    "service",
    "status",
    "created_at",
    "responded_at",
    "resolved_at",
    "sla_minutes",
    "reopen_count",
    "csat",
]


def safe_cell(value):
    text = str(value) if value is not None else ""
    if text.lstrip().startswith(("=", "+", "-", "@")):
        text = "'" + text
    return text


def export_snapshot(db, settings, client=None):
    if not settings.google_credentials or not settings.google_sheet_id:
        raise ValueError("Set GOOGLE_CREDENTIALS_FILE and GOOGLE_SHEET_ID first")
    if client is None:
        import gspread

        client = gspread.service_account(
            filename=settings.google_credentials, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
    rows = Service(db).list_requests({"id": 0, "role": "manager", "department_id": None})
    values = [HEADERS] + [
        [
            safe_cell(r[k])
            for k in (
                "id",
                "department_name",
                "category_name",
                "service",
                "status",
                "created_at",
                "responded_at",
                "resolved_at",
                "sla_minutes",
                "reopen_count",
                "csat",
            )
        ]
        for r in rows
    ]
    sheet = client.open_by_key(settings.google_sheet_id)
    try:
        worksheet = sheet.worksheet("Portfolio Requests")
    except Exception as error:
        import gspread

        if not isinstance(error, gspread.WorksheetNotFound):
            raise
        worksheet = sheet.add_worksheet("Portfolio Requests", rows=max(200, len(values)), cols=len(HEADERS))
    # One API batch clears old values and writes the new snapshot together.
    sheet.values_batch_update(
        {
            "valueInputOption": "RAW",
            "data": [
                {
                    "range": "'Portfolio Requests'!A1:K" + str(max(worksheet.row_count, len(values))),
                    "values": values + [[""] * len(HEADERS)] * max(0, worksheet.row_count - len(values)),
                }
            ],
        }
    )
    return len(rows)
