from unittest.mock import MagicMock

import pytest

from app.config import Settings
from app.sheets import export_snapshot, safe_cell


@pytest.mark.parametrize("value", ["=IMPORTXML('x')", "+1", "-1", "@SUM(A1)", "  =A1"])
def test_formula_injection_guard(value):
    assert safe_cell(value).startswith("'")


def test_export_uses_raw_values_and_omits_personal_data(domain):
    db, svc, guest = domain
    svc.create_request(guest, "amenities", "Extra towels", "Private detail")
    client = MagicMock()
    client.open_by_key.return_value.worksheet.return_value.row_count = 5
    assert (
        export_snapshot(db, Settings(google_credentials="private-file", google_sheet_id="test-sheet"), client)
        == 1
    )
    payload = client.open_by_key.return_value.values_batch_update.call_args.args[0]
    assert payload["valueInputOption"] == "RAW"
    assert "Fictional Guest" not in str(payload) and "Private detail" not in str(payload)
    assert len(payload["data"][0]["values"]) == 5


def test_export_failure_preserves_local_request(domain):
    db, svc, guest = domain
    svc.create_request(guest, "amenities", "Extra towels", "Please")
    client = MagicMock()
    client.open_by_key.side_effect = RuntimeError("Offline")
    with pytest.raises(RuntimeError):
        export_snapshot(db, Settings(google_credentials="private", google_sheet_id="test"), client)
    with db.connect() as c:
        assert c.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 1
