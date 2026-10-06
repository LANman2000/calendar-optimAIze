import datetime
from src.caldav_client import CalDAVClient
from src.event_parser import EventParser
from src.ai_analyzer import AIAnalyzer
from src.model_client import GroqModelClient


def main():
    print("\n=== Connecting to iCloud CalDAV ===")
    caldav = CalDAVClient()
    caldav.connect()

    print("Connected. Fetching calendars...")
    calendars = caldav.list_calendars()
    print(f"Available calendars: {calendars}")

    # Pull events for the next 7 days
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=7)

    print(f"\nFetching events from {start} to {end}...")
    raw_ics = caldav.fetch_events(start, end)
    print(f"Fetched {len(raw_ics)} raw ICS entries.")

    # Parse ICS → JSON
    print("\n=== Parsing events ===")
    parser = EventParser()
    events = parser.parse_ics_list(raw_ics)
    print(f"Parsed {len(events)} events.")

    # Send JSON → Groq model
    print("\n=== Sending to AI model ===")
    model = GroqModelClient()
    analyzer = AIAnalyzer(model)
    suggestions = analyzer.analyze(events)

    print("\n=== Weekly Optimization Plan ===\n")
    print(suggestions)


if __name__ == "__main__":
    main()
