from __future__ import annotations

import builtins
import io
import re
import sys
from dataclasses import dataclass
from typing import Any, Mapping

import pandas as pd


def extract_python_code(text: str) -> str:
    """Extract first python code block from markdown-ish text."""

    code_blocks = re.findall(r"```(?:python)?(.*?)```", text, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    return text.strip()


@dataclass(frozen=True)
class ExecResult:
    stdout: str
    error: str
    show_graphic: bool


def execute_user_code(
    *,
    code: str,
    data: pd.DataFrame,
    plt: Any,
    save_plot_path: str | None = None,
    extra_globals: Mapping[str, Any] | None = None,
) -> ExecResult:
    """Execute code with a controlled globals dict and capture stdout.

    Note: this intentionally keeps behaviour close to the workshop steps.
    """

    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    sys.stdout = redirected_output

    show_graphic = False
    error_msg = ""

    try:
        exec_globals: dict[str, Any] = {"data": data, "pd": pd, "plt": plt}
        if extra_globals:
            exec_globals.update(dict(extra_globals))

        getattr(builtins, "exec")(code, exec_globals)  # nosec B102

        if save_plot_path and getattr(plt, "get_fignums", None) and plt.get_fignums():
            plt.savefig(save_plot_path)
            plt.close()
            show_graphic = True

    except (
        SyntaxError,
        NameError,
        TypeError,
        ValueError,
        KeyError,
        AttributeError,
        IndexError,
        ZeroDivisionError,
        RuntimeError,
        ImportError,
    ) as ex:
        error_msg = f"Error executing code:\n{ex}"

    finally:
        sys.stdout = old_stdout

    return ExecResult(
        stdout=redirected_output.getvalue(), error=error_msg, show_graphic=show_graphic
    )
