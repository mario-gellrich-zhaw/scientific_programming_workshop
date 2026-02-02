from __future__ import annotations

import matplotlib

# Must be set before importing pyplot.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402


def configure_plot_style() -> None:
    """Configure default plot style for server-side rendering."""

    plt.style.use("dark_background")
