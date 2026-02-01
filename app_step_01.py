"""Augmented Analytics Flask demo app.

This module - when fully developed - sets up a Flask web application that
interacts with an OpenAI chat model. It loads an OpenAI API key from a .env
file, and allows users to submit prompts.
"""

import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from openai import OpenAI, OpenAIError

# Initialize Flask app
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
    """Main route of the web application."""

    gpt_response = ""

    if request.method == "POST":
        user_prompt = request.form.get("prompt", "")

        # Context prompt for GPT, describing the DataFrame
        prompt_for_gpt = (
            "You have a pandas DataFrame called 'data' "
            "loaded from './data/autoscout24_data.csv'. "
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
        except OpenAIError as e:  # pylint: disable=broad-exception-caught
            gpt_response = f"Error calling OpenAI API: {str(e)}"

    return render_template("index_step_01.html", gpt_response=gpt_response)


if __name__ == "__main__":
    app.run(debug=True)
