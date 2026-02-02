from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    """Return the repository/project root directory.

    Assumes this file lives in `src/scientific_programming_workshop/`.
    """

    return Path(__file__).resolve().parents[2]


ROOT_DIR = project_root()
DATA_DIR = ROOT_DIR / "data"
TEMPLATES_DIR = ROOT_DIR / "templates"
STATIC_DIR = ROOT_DIR / "static"

CSV_PATH = DATA_DIR / "autoscout24_data.csv"
GRAPHIC_PATH = STATIC_DIR / "graphic.png"
