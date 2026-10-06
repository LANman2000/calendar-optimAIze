import datetime
import os
from dotenv import load_dotenv

from caldav import DAVClient
from caldav.lib.error import AuthorizationError, NotFoundError

load_dotenv()
class CalDAVClient:
    """
    Handles connection to iCloud CalDAV and event retrieval.
    """

    def __init__(self):
        self.username = os.getenv("APPLE_ID_EMAIL")
        self.password = os.getenv("APPLE_APP_PASSWORD")

        # Exception handling
        if not self.username or not self.password:
            raise Exception("Apple ID email or app-specific password not set in environment variables.")
        
        self.client = None
        self.principal = None
        self.calendars = None

    def connect(self):
        """
        Connect to iCloud CalDAV using app-specific password.
        """
        try:
            self.client = DAVClient(
                url="https://caldav.icloud.com/",
                username=self.username,
                password=self.password
            )
            self.principal = self.client.principal()
            self.calendars = self.principal.calendars()
            return True

        except AuthorizationError:
            raise Exception("Invalid Apple ID or app-specific password.")

        except Exception as e:
            raise Exception(f"CalDAV connection failed: {e}")

    def list_calendars(self):
        """
        Returns a list of calendar names.
        """
        if not self.calendars:
            raise Exception("Not connected. Call connect() first.")

        return [cal.name for cal in self.calendars]

    def get_calendar(self, index: int = 0):
        """
        Returns a specific calendar object.
        Default: first calendar (usually your main one).
        """
        if not self.calendars:
            raise Exception("Not connected. Call connect() first.")

        try:
            return self.calendars[index]
        except IndexError:
            raise Exception("Calendar index out of range.")

    def fetch_events(self, start: datetime.datetime, end: datetime.datetime, calendar_index: int = 0):
        """
        Fetch events between two datetimes.
        Returns raw ICS strings.
        """
        calendar = self.get_calendar(calendar_index)

        try:
            events = calendar.date_search(start, end)
        except NotFoundError:
            return []

        raw_ics_list = []
        for event in events:
            raw_ics_list.append(event.data)

        return raw_ics_list


# Example usage
if __name__ == "__main__":
    import json

    client = CalDAVClient()
    client.connect()

    print("Calendars:", client.list_calendars())

    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=7)

    events = client.fetch_events(start, end)
    print(f"Fetched {len(events)} events.")
