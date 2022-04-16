import typing
from datetime import datetime, timedelta
from icalevents.icaldownload import ICalDownload
from icalevents.icalparser import parse_events, Event, normalize

from MAL_Remainder.common_utils import ensure_data, current_executable
from MAL_Remainder.utils import SETTINGS
import logging

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


def to_frame(events: typing.List[Event]) -> typing.Tuple[list, list]:
    """
    converts a list of events to a pandas dataframe
    """
    local_zone = datetime.today().astimezone().tzinfo

    events = [
        event for event in events if not event.all_day
    ]

    started = [
        [normalize(event.start, local_zone), event.description, event.summary] for event in events if
        event.start.day == datetime.today().day
    ]

    ended = [
        normalize(event.end, local_zone) for event in events
        if event.end.day == datetime.today().day
    ]
    return started, ended


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


# I guess you don't need to worry about timezones 🤡

def from_now():
    internal = quick_save()

    if not internal:
        return

    return to_frame(
        parse_events(
            internal,
            start=datetime.now(),
            default_span=timedelta(days=1)
            # schedules events within 1 day. After that it needs to reschedule
        )
    )


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

    logging.info("Scheduling Events")
    started, ended = from_now()

    if not ended:
        return

    triggers_for_end = ",".join(
        event_time.strftime(FORMAT) for event_time in ended
    )

    current_executable(
        "-sch", "-arguments", triggers_for_end
    )

    say_we_are_done_today()


if __name__ == "__main__":
    print(from_now())
