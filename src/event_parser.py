from ics import Calendar
from typing import Any, Dict, List, Optional

class EventParser:
    """
    Converts raw ICS strings into structured JSON events.
    """

    def __init__(self):
        pass

    def parse_ics_list(self, raw_ics_list: List[str]) -> List[Dict[str, Any]]:
        """
        Takes a list of raw ICS strings and returns a list of event dictionaries.
        """
        parsed_events = []

        for index, raw_ics in enumerate(raw_ics_list, start=1):
            try:
                calendar = Calendar(raw_ics)

                for event in calendar.events:
                    parsed_events.append(self._parse_single_event(event))

            except Exception as exc:
                raise ValueError(f"Failed to parse ICS entry {index}: {exc}") from exc

        return parsed_events

    def _parse_single_event(self, event: Any) -> Dict[str, Any]:
        """
        Converts a single ICS event into a JSON-friendly dictionary.
        """
        return {
            "name": event.name or "Untitled Event",
            "begin": self._to_iso(event.begin),
            "end": self._to_iso(event.end),
            "duration_minutes": self._duration_minutes(event),
            "location": event.location or None,
            "description": event.description or None,
        }

    def _to_iso(self, dt_obj: Any) -> Optional[str]:
        """
        Converts datetime-like objects to ISO strings.
        """
        if not dt_obj:
            return None
        try:
            return dt_obj.isoformat()
        except (AttributeError, TypeError, ValueError):
            return str(dt_obj)

    def _duration_minutes(self, event: Any) -> Optional[int]:
        """
        Returns event duration in minutes.
        """
        try:
            return int(event.duration.total_seconds() // 60)
        except (AttributeError, TypeError, ValueError):
            return None


# Example
if __name__ == "__main__":
    sample_ics = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//CalendarOptimize//EN
BEGIN:VEVENT
SUMMARY:Gym Session
DTSTART:20261004T180000
DTEND:20261004T190000
LOCATION:Fitness Center
DESCRIPTION:Leg day
END:VEVENT
END:VCALENDAR
"""

    parser = EventParser()
    events = parser.parse_ics_list([sample_ics])
    print(events)