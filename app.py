from flask import Flask, render_template, request
import os

import anthropic
import markdown2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Claude AI API details
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
API_URL = "https://api.anthropic.com/v1/messages"

# Hardcoded prompt for Claude
SYSTEM_PROMPT_ORIG = """
You are an expert at reviewing and improving event invitation drafts.
Your task is to review the draft invitation text and suggest improvements to make it:
1. Clear and concise
2. Engaging and compelling
3. Free of grammatical or spelling errors
4. Professional in tone

Provide specific suggestions for improvement and then an improved version of the invitation.
"""

SYSTEM_PROMPT = """
You are a senior content writer who works for public services in the UK.
You aim for a reading age of 9 years old, so the materials produced can be understood by as many people
as possible and the public services will have the highest possible engagement with the materials.
You follow all the best practice for British English.

You have been given invite materials for a citizens' assembly to review and improve on.
Produce your recommendations by showing a snippet of the original text and then showing your suggestion. Also give the reasons for the suggested change.
"""


@app.route("/", methods=["GET"])
def index():
    """Handle GET request - display the form."""
    return render_template("index.html")


def call_claude_api(text_content) -> tuple[bool, str]:
    """
    Call the Claude AI API with the provided text content.

    Args:
        text_content (str): The text to send to Claude AI

    Returns:
        tuple: (success, response_or_error)
            - success: Boolean indicating if the API call was successful
            - response_or_error: Either the Claude response text or an error message
    """
    # Check for API key
    if not ANTHROPIC_API_KEY:
        return False, "API key not configured. Set the ANTHROPIC_API_KEY environment variable or in a .env file."

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    try:
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=20000,
            temperature=1,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Here is my draft invitation. Please review and improve it:\n\n{text_content}"
                        }
                    ]
                }
            ]
        )

        return True, result_to_html(message.content)
    except anthropic.APIConnectionError as e:
        msg = f"The server could not be reached: {e.__cause__}"
        return False, msg
    except anthropic.RateLimitError as e:
        msg = "A 429 status code was received; we should back off a bit."
        return False, msg
    except anthropic.APIStatusError as e:
        msg = "Another non-200-range status code was received. Code {e.status_code}, Response: {e.response}"
        return False, msg
    except Exception as e:
        return False, f"Error: {str(e)}"


def result_to_html(result: list[anthropic.types.TextBlock]) -> str:
    if len(result) != 1 or not hasattr(result[0], "text"):
        return str(result)
    # try to convert the response from markdown to HTML
    try:
        return markdown2.markdown(result[0].text)
    except Exception as e:
        # if it isn't markdown, just leave it raw
        print(f"failed to convert markdown, {e}")
        return str(result)


@app.route("/", methods=["POST"])
def process_invitation():
    """Handle POST request - process the submitted form and get Claude AI response."""
    # Get the draft invitation from the form
    draft_invitation = request.form.get("draft_invitation", "")

    if not draft_invitation:
        return render_template("index.html", error="Please enter a draft invitation.")

    # Call Claude API
    success, result = call_claude_api(draft_invitation)

    if success:
        return render_template("index.html", response=result, draft=draft_invitation)
    else:
        return render_template("index.html", error=result, draft=draft_invitation)


if __name__ == "__main__":
    # Check for API key on startup
    if not ANTHROPIC_API_KEY:
        print("Warning: ANTHROPIC_API_KEY environment variable is not set")

    # Run the Flask app
    app.run(debug=True)
