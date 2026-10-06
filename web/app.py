from flask import Flask, render_template
import datetime

from src.caldav_client import CalDAVClient
from src.event_parser import EventParser
from src.ai_analyzer import AIAnalyzer
from src.model_client import GroqModelClient

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run")
def run_pipeline():
    caldav = CalDAVClient()
    caldav.connect()

    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=7)
    raw_ics = caldav.fetch_events(start, end)

    parser = EventParser()
    events = parser.parse_ics_list(raw_ics)

    model = GroqModelClient()
    analyzer = AIAnalyzer(model)
    suggestions = analyzer.analyze(events)

    return render_template("index.html", output=suggestions)

if __name__ == "__main__":
    app.run(debug=True)
