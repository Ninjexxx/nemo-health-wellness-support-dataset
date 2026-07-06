"""Project configuration values."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SYNTHETIC_DATA_DIR = PROJECT_ROOT / "data" / "synthetic"
DEFAULT_OUTPUT_PATH = SYNTHETIC_DATA_DIR / "health_wellness_eval.jsonl"
REPORTS_DIR = PROJECT_ROOT / "reports"
DEFAULT_REPORT_PATH = REPORTS_DIR / "latest_dataset_review.md"
