"""Configuration has no import-time network calls and never logs secrets."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    database: Path = Path("data/hotel.sqlite")
    demo: bool = True
    bot_token: str = ""
    extended_profile: bool = False
    menu_file_id: str = ""
    google_credentials: str = ""
    google_sheet_id: str = ""

    @classmethod
    def from_env(cls):
        load_dotenv()
        return cls(
            database=Path(os.getenv("DATABASE_PATH", "data/hotel.sqlite")),
            demo=os.getenv("DEMO_MODE", "true").lower() == "true",
            bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            extended_profile=os.getenv("COLLECT_EXTENDED_PROFILE", "false").lower() == "true",
            menu_file_id=os.getenv("MENU_FILE_ID", ""),
            google_credentials=os.getenv("GOOGLE_CREDENTIALS_FILE", ""),
            google_sheet_id=os.getenv("GOOGLE_SHEET_ID", ""),
        )
