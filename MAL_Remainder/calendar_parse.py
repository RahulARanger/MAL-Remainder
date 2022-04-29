import typing
from datetime import datetime, timedelta
from icalevents.icaldownload import ICalDownload
from icalevents.icalparser import parse_events, normalize, Event
from MAL_Remainder.common_utils import ensure_data, current_executable
import logging


"""
This Module is for datetime related things and most specifically for parsing calendar files .ics

Can also schedule events in your local machine indirectly.
"""


def quick_save(url: str = "") -> str:
    """
    :param url: if fetch from URL then specify its url else leave it empty.
    :return: Raw string from ICS file either from local or from embedded URL.
    """
    source = ensure_data() / "source.ics"
    source.touch()

    is_local = bool(url)
    url = source if is_local else url

    parser = ICalDownload()
    if not is_local:
        internal = parser.data_from_url(url)
        source.write_text(internal)
        return internal

    internal = url.read_text()
    parser.data_from_file(url) if internal else ...
    return internal


def _events(start=datetime.now(), default_span=timedelta(days=1)) -> typing.Generator[Event, None, None]:
    """
    Yields all events in the given time span. But also make sures the events are not all day along.

    :param start: Start looking for events from this time.
    :param default_span: Default time span to look for events.
    :return:Generator of Events
    """
    internal = quick_save()

    if not internal:
        return

    yield from [event for event in
                parse_events(
                    internal,
                    start=start, default_span=default_span
                ) if not event.all_day]


def from_now() -> typing.Optional[typing.List[datetime]]:
    """
    Same as getting events for now until the next day, but it makes sure to normalize with your local time zone
    :return: List of datetime objects of events that are going to end today.
    """
    events = list(_events())
    local_zone = datetime.today().astimezone().tzinfo

    # started = [
    #     normalize(event.start, local_zone) for event in events
    # ]
    ended = [
        normalize(event.end, local_zone) for event in events
    ]

    return ended


FORMAT: str = "%Y-%m-%d %H:%M:%S"


def schedule_events() -> typing.NoReturn:
    """
    Indirectly Schedules events in your system by passing in the timestamps for today.

    :return: None
    """
    logging.info("Scheduling Events")
    ended = from_now()

    if not ended:
        return

    triggers_for_end = ",".join(
        event_time.strftime(FORMAT) for event_time in ended
    )

    current_executable(
        "-sch", "-arguments", triggers_for_end
    )


def stamp() -> str:
    """
    returns the timestamp for now
    :return:
    """
    return datetime.now().strftime(FORMAT)


def update_now_in_seconds(x: dict):
    x["now"] = int(datetime.now().timestamp())
    return x


if __name__ == "__main__":
    # This is needed for automatic refresh
    schedule_events()
