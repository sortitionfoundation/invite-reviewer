from flask import Flask, render_template, request, jsonify
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Claude AI API details
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
API_URL = "https://api.anthropic.com/v1/messages"

# Hardcoded prompt for Claude
SYSTEM_PROMPT = """
You are an expert at reviewing and improving event invitation drafts. 
Your task is to review the draft invitation text and suggest improvements to make it:
1. Clear and concise
2. Engaging and compelling
3. Free of grammatical or spelling errors
4. Professional in tone

Provide specific suggestions for improvement and then an improved version of the invitation.
"""

@app.route("/", methods=["GET"])
def index():
    """Handle GET request - display the form."""
    return render_template("index.html")


def call_claude_api(text_content):
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
    
    try:
        # Prepare the payload for Claude AI
        payload = {
            "model": "claude-3-sonnet-20240229",
            "system": SYSTEM_PROMPT,
            "messages": [
                {
                    "role": "user",
                    "content": f"Here is my draft invitation. Please review and improve it:\n\n{text_content}"
                }
            ],
            "max_tokens": 4000
        }
        
        # Make request to Claude AI API
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload
        )
        
        # Check for successful response
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get("content", [{}])[0].get("text", "No response received")
            return True, ai_response
        else:
            error_message = f"API Error: {response.status_code} - {response.text}"
            return False, error_message
            
    except Exception as e:
        return False, f"Error: {str(e)}"


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
