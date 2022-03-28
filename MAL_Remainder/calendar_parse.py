import typing
import pandas
from datetime import datetime

from icalevents.icaldownload import ICalDownload
from icalevents.icalparser import parse_events, Event, normalize

from MAL_Remainder.common_utils import ensure_data, current_executable
from MAL_Remainder.utils import SETTINGS

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
    local_zone = datetime.today().astimezone().tzinfo
    return pandas.DataFrame(
        [
            (
                event.uid,
                event.summary,
                normalize(event.start, local_zone),
                normalize(event.end, local_zone),
                event.description
            )
            for event in events
            if not event.all_day
        ], columns=["uid", "title", "started", "ended", "summary"]
    )


def quick_save(url="", is_local=True):
    source = ensure_data() / "source.ics"
    source.touch()

    url = url if url else source

    parser = ICalDownload()
    if not is_local:
        internal = parser.data_from_url(url)
        source.write_text(internal)
        return internal

    internal = url.read_text()
    parser.data_from_file(url) if internal else ...
    return internal


def _events(internal, start_date: datetime, end_date: datetime):
    return to_frame(
        parse_events(
            internal,
            start=normalize(start_date),
            end=normalize(end_date)
            # don't schedule things based on the microseconds :)
        ) if internal else []
    )


def from_now():
    return _events(quick_save(), datetime.now(), _end_of_day())


def today():
    return _events(quick_save(), _start_of_day(), _end_of_day())


FORMAT = "%Y-%m-%d %H:%M:%S"


def say_we_are_done_today():
    SETTINGS["schedule_events"] = datetime.now().strftime(FORMAT)


def are_we_done_today():
    event_stamp = SETTINGS["schedule_events"]

    if not event_stamp:
        return False

    return (datetime.today() - datetime.strptime(event_stamp, FORMAT)).days == 0


def schedule_events(force=False):
    if are_we_done_today() and not force:
        return

    frame = from_now()
    triggers_for_end = ",".join(frame["ended"].dt.strftime("%H:%M:%S") if frame["ended"].size else [])
    reason_for_failure = current_executable("-sch", "-triggers_for_end", triggers_for_end)

    say_we_are_done_today()
    return reason_for_failure


if __name__ == "__main__":
    schedule_events()
