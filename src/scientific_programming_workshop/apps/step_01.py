"""Flask app implementation for workshop step 01."""

from __future__ import annotations

from flask import Flask, render_template, request
from openai import OpenAIError

from ..llm_client import get_openai_client
from ..paths import STATIC_DIR, TEMPLATES_DIR


def create_app() -> Flask:
    """Create and configure the Step 01 Flask application."""
    flask_app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
    )

    @flask_app.route("/", methods=["GET", "POST"])
    def index():
        gpt_response = ""

        if request.method == "POST":
            user_prompt = request.form.get("prompt", "")

            prompt_for_gpt = (
                "You have a pandas DataFrame called 'data' "
                "loaded from './data/autoscout24_data.csv'. "
                "Please write Python code that works with this DataFrame.\n\n"
                f"User Prompt: {user_prompt}"
            )

            try:
                client = get_openai_client()
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": prompt_for_gpt}],
                    max_tokens=300,
                )
                gpt_response = response.choices[0].message.content or ""
            except ValueError as e:
                gpt_response = str(e)
            except OpenAIError as e:  # pylint: disable=broad-exception-caught
                gpt_response = f"Error calling OpenAI API: {str(e)}"

        return render_template("index_step_01.html", gpt_response=gpt_response)

    return flask_app


app = create_app()
