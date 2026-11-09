import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

GNANI_API_KEY = os.getenv("GNANI_API_KEY")

if not GNANI_API_KEY:
    raise RuntimeError(
        "GNANI_API_KEY is missing. Please check your .env file."
    )

APP_NAME = "ArogyaDhwani"
APP_VERSION = "1.0.0"

UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)