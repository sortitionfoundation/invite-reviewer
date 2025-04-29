# Invitation Reviewer with Claude AI

A simple Flask application that uses Anthropic's Claude AI to review and improve event invitation drafts.

## Features

- Web interface for submitting draft invitations
- Integration with Claude AI for intelligent review and suggestions
- Improved version of the invitation provided by Claude AI

## Prerequisites

- Python 3.8 or higher
- Anthropic API key (Claude AI)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/invitation-reviewer.git
   cd invitation-reviewer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set your Anthropic API key by either:
   
   a) Creating a `.env` file in the project root with the following content:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```
   
   b) Setting it as an environment variable:
   ```
   # On Windows
   set ANTHROPIC_API_KEY=your-api-key-here
   
   # On macOS/Linux
   export ANTHROPIC_API_KEY=your-api-key-here
   ```

## Project Structure

```
invitation-reviewer/
│
├── app.py              # Main Flask application with modular design
├── requirements.txt    # Project dependencies
├── README.md           # This file
├── .env.example        # Example environment variables file
└── templates/
    └── index.html      # HTML template for the web interface
```

## Running the Application

1. Make sure you have set your Anthropic API key as described in the Installation section.

2. Run the Flask application:
   ```
   python app.py
   ```

3. Open your web browser and navigate to `http://127.0.0.1:5000/`

4. Paste your draft invitation into the form and click "Analyze with Claude AI" to receive suggestions for improvement.

## Modifying the Prompt

If you want to change how Claude evaluates the invitations, you can modify the `SYSTEM_PROMPT` variable in `app.py`. This allows you to customize the instructions given to Claude AI.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
