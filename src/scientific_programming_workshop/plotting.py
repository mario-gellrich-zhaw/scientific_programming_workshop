"""Plotting configuration for server-side rendering."""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt

# Must be set before importing pyplot.
matplotlib.use("Agg")


def configure_plot_style() -> None:
    """Configure default plot style for server-side rendering."""
    plt.style.use("dark_background")
