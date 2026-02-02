from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


@pytest.fixture(name="flask_app_step_04")
def _flask_app_step_04():
    module = importlib.import_module("scientific_programming_workshop.apps.step_04")  # pyright: ignore[reportMissingImports]
    create_app = getattr(module, "create_app")

    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def client_step_04(flask_app_step_04):
    return flask_app_step_04.test_client()
