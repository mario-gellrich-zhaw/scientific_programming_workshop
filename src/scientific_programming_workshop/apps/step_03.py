from __future__ import annotations

from flask import Flask, render_template, request
from openai import OpenAIError

from ..code_exec import ExecResult, execute_user_code, extract_python_code
from ..data_loading import describe_dataframe, load_autoscout_data
from ..llm_client import get_openai_client
from ..paths import GRAPHIC_PATH, STATIC_DIR, TEMPLATES_DIR
from ..plotting import configure_plot_style, plt


def create_app() -> Flask:
    configure_plot_style()

    flask_app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
    )

    @flask_app.route("/", methods=["GET", "POST"])
    def index():
        gpt_response = ""
        execution_result = ""
        code_to_execute = ""
        show_graphic = False

        if GRAPHIC_PATH.exists():
            GRAPHIC_PATH.unlink()

        data = load_autoscout_data()
        data_struct_desc = describe_dataframe(data)

        if request.method == "POST":
            user_prompt = request.form.get("prompt", "")

            prompt_for_gpt = (
                "You have a pandas DataFrame called 'data' "
                "loaded from './data/autoscout24_data.csv'. "
                "Here is the structure of the DataFrame:\n\n"
                f"{data_struct_desc}\n\n"
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
                gpt_response = response.choices[0].message.content
                code_to_execute = extract_python_code(gpt_response)

                result: ExecResult = execute_user_code(
                    code=code_to_execute,
                    data=data,
                    plt=plt,
                    save_plot_path=str(GRAPHIC_PATH),
                )

                show_graphic = result.show_graphic
                execution_result = result.error or result.stdout

            except ValueError as e:
                gpt_response = str(e)
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

    return flask_app


app = create_app()
