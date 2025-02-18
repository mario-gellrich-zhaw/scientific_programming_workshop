"""
This module sets up a Flask web application that interacts with the OpenAI 
GPT-3.5-turbo model. It loads an OpenAI API key from a credentials file, reads 
data from a CSV file, and allows users to submit prompts to generate Python code 
that works with the DataFrame loaded from the CSV file. The generated code is 
then executed, and the results are displayed on a web page.
"""

# Import necessary libraries
import json
import openai
import pandas as pd
from flask import Flask, render_template, request

# Set up the Flask app
app = Flask(__name__)

# Load OpenAI API key from credentials.json
try:
    with open('./data/credentials.json', encoding='utf-8') as file:
        credentials = json.load(file)
        API_KEY = credentials['openai']['api_key']
except FileNotFoundError as exc:
    raise ValueError(
        "Please provide OpenAI API key in the credentials.json file."
    ) from exc

# Set the OpenAI API key
openai.api_key = API_KEY

# Define the main route of the web application
@app.route("/", methods=["GET", "POST"])
def index():
    """Main route of the web application"""

    gpt_response = ""

    # Load .csv data (needed when Python code is executed)
    data = pd.read_csv("./data/autoscout24_data.csv")

    if request.method == "POST":
        user_prompt = request.form.get("prompt", "")

        # Small context instructing GPT about the DataFrame
        prompt_for_gpt = (
            "You have a pandas DataFrame called 'data' loaded "
            "from 'autoscout24_data.csv'. Please write Python code "
            "that works with this DataFrame.\n\n"
            f"User Prompt: {user_prompt}"
        )

        # Send prompt to GPT
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt_for_gpt}],
                max_tokens=300
            )
            gpt_response = response.choices[0].message['content']
        except openai.error.OpenAIError as e:
            gpt_response = f"Error calling OpenAI API: {str(e)}"

    return render_template("index.html", gpt_response=gpt_response)


if __name__ == "__main__":
    app.run(debug=True)
