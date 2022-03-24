import typing
import pandas
from icalevents.icaldownload import ICalDownload
from icalevents.icalparser import parse_events, Event
from common_utils import ensure_data
from datetime import datetime
from collections import namedtuple

CalendarEvent = namedtuple("Event", ["uid", "name", "started", "ended"])

"""
NOTES regarding the ics file,

every line in ics is of form; name, parameter, value
common to see lines are (name, value); parameter is optional 

examples:
~~~~~~~~~

VERSION:6.9
ATTENDEE;CN=Max Rasmussen;ROLE=REQ-PARTICIPANT:MAILTO:example@example.com


Calendar has Components in which each component has a sub-component

Root Component is like this ...

BEGIN:VCALENDAR
... vcalendar properties ...
END:VCALENDAR


VEVENT is a component(which we need)

it looks like this 

BEGIN:VEVENT
... vevent properties ...
END:VEVENT

# NOTE: we won't edit the properties of the VCALENDAR, but we may for the VEVENT
"""


def _start_of_day(date=datetime.now()):
    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def _end_of_day(date=datetime.now()):
    return date.replace(hour=23, minute=59, second=59, microsecond=0)


def to_frame(events: typing.List[Event]) -> pandas.DataFrame:
    """
    converts a list of events to a pandas dataframe
    """
    return pandas.DataFrame(
        [
            {
                "uid": event.uid,
                "title": event.summary,
                "started": event.start,
                "ended": event.end,
                "summary": event.description
            }
            for event in events if not event.all_day
        ]
    )


class SchCalendar:
    def __init__(self, url="", is_local=False):
        self.source = ensure_data() / "source.ics"

        is_local = is_local if url else True
        url = url if url else self.source

        parser = ICalDownload()
        self.internal = parser.data_from_file(url) if is_local else parser.data_from_url(url)
        ... if is_local else self.source.write_text(self.internal)

    def _events(self, start_date: datetime, end_date: datetime):
        zone = start_date.astimezone().tzinfo
        return to_frame(parse_events(
            self.internal,
            start=start_date,
            end=end_date
            # don't schedule things based on the microseconds :)
        ))

    def from_now(self):
        return self._events(datetime.now(), _end_of_day())

    def today(self):
        return self._events(_start_of_day(), _end_of_day())

    def save_from_now(self):
        return self.from_now().to_csv(self.source.parent / "from_now.csv", index=False)


if __name__ == "__main__":
    # calendar = SchCalendar()
    calendar = SchCalendar(
        "https://calendar.google.com/calendar/ical/1jh19esq880ljnl7dn6b3l8ceo%40group.calendar.google.com/public/basic.ics")
    calendar.save_from_now()
