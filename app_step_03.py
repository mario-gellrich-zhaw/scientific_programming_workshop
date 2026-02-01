"""Augmented Analytics Flask demo app (step 03).

This module sets up a Flask web application that interacts with an OpenAI chat
model. It loads an OpenAI API key from a .env file, reads data from a CSV file,
and allows users to submit prompts. Model-generated code is executed and the
result is displayed.
"""

# pyright: reportGeneralTypeIssues=false

import builtins
import io
import os
import re
import sys

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template, request
from openai import OpenAI, OpenAIError

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# Set dark background for all plots
plt.style.use('dark_background')

app = Flask(__name__)

# Load OpenAI API key from .env (or environment)
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError(
        "Please set OPENAI_API_KEY in a .env file (or as an environment "
        "variable)."
    )

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the prompt UI and show model output."""

    gpt_response = ""
    execution_result = ""
    code_to_execute = ""
    show_graphic = False  # Initialize with False

    # Remove any existing graphics
    if os.path.exists("./static/graphic.png"):
        os.remove("./static/graphic.png")

    # Load CSV data
    data = pd.read_csv("./data/autoscout24_data.csv")

    # Create a string that describes the structure of the DataFrame
    data_struct_desc = f"Columns: {list(data.columns)}\n\n"
    data_struct_desc += f"Data types:\n{data.dtypes}\n\n"
    data_struct_desc += f"Example rows:\n{data.head(5).to_string(index=False)}"

    if request.method == "POST":
        user_prompt = request.form.get("prompt", "")

        # Context prompt for GPT, describing the DataFrame
        prompt_for_gpt = (
            "You have a pandas DataFrame called 'data' "
            "loaded from './data/autoscout24_data.csv'. "
            "Here is the structure of the DataFrame:\n\n"
            f"{data_struct_desc}\n\n"
            "Please write Python code that works with this DataFrame.\n\n"
            f"User Prompt: {user_prompt}"
        )

        # Call GPT-3.5-turbo via OpenAI's ChatCompletion endpoint
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt_for_gpt}],
                max_tokens=300,
            )
            # Extract the model's response
            gpt_response = response.choices[0].message.content

            # Extract code between triple backticks
            code_blocks = re.findall(
                r"```(?:python)?(.*?)```",
                gpt_response,
                re.DOTALL,
            )
            if code_blocks:
                code_to_execute = code_blocks[0].strip()
            else:
                # If no code blocks found, treat the entire response as code
                code_to_execute = gpt_response.strip()

            # Prepare to capture stdout
            old_stdout = sys.stdout
            redirected_output = io.StringIO()
            sys.stdout = redirected_output

            try:
                exec_globals = {
                    "data": data,
                    "pd": pd,
                    "plt": plt,
                }
                getattr(builtins, "exec")(code_to_execute, exec_globals)  # nosec B102

                # Check if a plot was created by inspecting the current figure
                if plt.get_fignums():  # Check if any figures exist
                    plt.savefig("./static/graphic.png")
                    plt.close()
                    show_graphic = True
                else:
                    show_graphic = False
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
            ) as ex:  # pylint: disable=broad-exception-caught  # type: ignore
                execution_result = f"Error executing code:\n{ex}"
            else:
                # Capture print statements
                execution_result = redirected_output.getvalue()
            finally:
                # Restore stdout
                sys.stdout = old_stdout

        except OpenAIError as e:  # pylint: disable=broad-exception-caught
            gpt_response = f"Error calling OpenAI API: {str(e)}"

    return render_template(
        "index_step_03.html",
        prompt=request.form.get("prompt", ""),
        gpt_response=gpt_response,
        code_to_execute=code_to_execute,
        execution_result=execution_result,
        show_graphic=show_graphic,
    )


if __name__ == "__main__":
    app.run(debug=True)
