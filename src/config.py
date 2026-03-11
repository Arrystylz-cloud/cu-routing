"""Project configuration helpers."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MANUAL_DATA_DIR = DATA_DIR / "manual"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

DEFAULT_WALKING_SPEED_M_PER_MIN = 80.0
