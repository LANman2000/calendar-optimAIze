# Calendar Optimize

Calendar Optimize is a Python demo that reads events from an iCloud calendar using CalDAV, parses the event details, and asks a Groq-hosted language model for ideas to improve a weekly schedule. It can suggest opportunities for sleep, cooking, exercise, meals, and recovery based on the events it receives.

> **Demo status:** The current workflow generates a plan from calendar events. It does not edit or reschedule events in iCloud, and it is not yet an interactive chat for negotiating changes.

## Requirements

- Python 3.10 or later
- An iCloud account with Calendar enabled
- An Apple app-specific password (requires two-factor authentication)
- A Groq API key and access to a Groq model

## Setup

Clone the repository and open a terminal in its root directory:

```powershell
cd CalendarOptimize
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root. Do not commit this file:

```dotenv
APPLE_ID_EMAIL= apple-account-email
APPLE_APP_PASSWORD= apple-app-specific-password
GROQ_API_KEY= groq-api-key
AI_MODEL_NAME= model-id-available-to-groq-account
```

`AI_MODEL_NAME` must exactly match a model ID available to the Groq account. Check the current Groq model list in the Groq console; available models can change.

## Run the command-line demo

From the project root:

```powershell
python main.py
```

The script connects to CalDAV, fetches events from the first calendar for the next seven days, parses them, and prints the model's schedule suggestions.

## Run the Flask demo

From the project root:

```powershell
python -m web.app
```

Open <http://127.0.0.1:5000> in a browser and choose **Run Weekly Optimization**. The current web page runs the same fetch-and-analyze flow; it does not provide a chat interface.

The Flask development server is for local demonstration only. Do not deploy it with `debug=True`.

## Privacy and credentials

Calendar event names, times, locations, and descriptions may be sent to Groq as part of the analysis prompt. Use a test calendar or remove sensitive event details if you do not want to send them to the model provider.

- Never commit `.env`, app-specific passwords, or API keys.
- If a credential is exposed, revoke it and create a replacement.
- Avoid sharing full calendar data or unredacted logs when requesting help.

## Project structure

```text
.
├── main.py                 # Command-line workflow
├── requirements.txt        # Python dependencies
├── src/
│   ├── ai_analyzer.py      # Builds prompt and interprets model response
│   ├── caldav_client.py    # Connects to iCloud and fetches calendar events
│   ├── event_parser.py     # Converts ICS data to dictionaries
│   └── model_client.py     # Groq API client wrapper
└── web/
    ├── app.py              # Flask demo application
    └── templates/
        └── index.html      # Demo page
```

## Troubleshooting

- **Missing environment variable:** Confirm `.env` is in the project root and the variable names match the example above.
- **CalDAV Unauthorized:** Verify the Apple Account email and app-specific password. Do not use the normal Apple Account password.
- **Groq model not found:** Confirm `AI_MODEL_NAME` is an exact model ID currently available to  Groq account.
- **Import errors when running the web app:** Run `python -m web.app` from the repository root rather than `python web/app.py`.

## License

No license has been specified yet. Until one is added, do not assume this project is available for reuse or redistribution.
