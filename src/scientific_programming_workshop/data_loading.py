"""Data loading utilities for the workshop dataset."""

from __future__ import annotations

import pandas as pd

from .paths import CSV_PATH


def load_autoscout_data() -> pd.DataFrame:
    """Load the workshop CSV into a DataFrame."""
    return pd.read_csv(CSV_PATH)


def describe_dataframe(data: pd.DataFrame, max_rows: int = 5) -> str:
    """Create a compact, LLM-friendly description of a DataFrame."""
    description = f"Columns: {list(data.columns)}\n\n"
    description += f"Data types:\n{data.dtypes}\n\n"
    description += f"Example rows:\n{data.head(max_rows).to_string(index=False)}"
    return description
