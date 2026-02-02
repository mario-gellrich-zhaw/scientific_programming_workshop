"""Workshop entrypoint (step 01).

This file remains as a stable entrypoint for the workshop instructions.
The implementation lives in the `src/` package.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import TYPE_CHECKING, cast

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

if TYPE_CHECKING:
    from flask import Flask
else:
    Flask = object  # type: ignore[assignment]

try:
    _module = importlib.import_module("scientific_programming_workshop.apps.step_01")
except ModuleNotFoundError as e:
    missing = e.name or "<unknown>"
    raise ModuleNotFoundError(
        "A required dependency is missing while starting the app.\n\n"
        f"Missing module: {missing}\n"
        f"Python executable: {sys.executable}\n\n"
        "Fix:\n"
        "- Activate your virtualenv/conda env\n"
        "- Install dependencies: pip install -r requirements.txt\n"
    ) from e

app = cast(Flask, getattr(_module, "app"))

if __name__ == "__main__":
    app.run(debug=True)
