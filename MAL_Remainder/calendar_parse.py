import typing
from datetime import datetime, timedelta
from icalevents.icaldownload import ICalDownload
from icalevents.icalparser import parse_events, Event, normalize
from MAL_Remainder.common_utils import ensure_data, current_executable
from MAL_Remainder.utils import SETTINGS
import logging


def _events(start=datetime.now(), default_span=timedelta(days=1)):
    internal = quick_save()

    if not internal:
        return

    yield from [event for event in
                parse_events(
                    internal,
                    start=start, default_span=default_span
                ) if not event.all_day]


def previously():
    store = sorted(_events(
        start=datetime.now() - timedelta(days=1)
    ), key=lambda x: x.start)

    if not store:
        return -1

    length = len(store)
    left = 0
    right = length - 1

    asked = datetime.now().timestamp()

    while left <= right:
        mid = (left + right) // 2

        if store[mid].start.timestamp() == asked:
            return mid

        if store[mid].start.timestamp() < asked:
            left = mid + 1
        else:
            right = mid - 1

    return store[left] if left < length else store[right]


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


def from_now():
    internal = quick_save()

    if not internal:
        return

    local_zone = datetime.today().astimezone().tzinfo

    events = list(_events())

    started = [
        normalize(event.start, local_zone) for event in events
    ]

    ended = [
        normalize(event.end, local_zone) for event in events
    ]

    return started, ended


FORMAT = "%Y-%m-%d %H:%M:%S"


def say_we_are_done_today(say=False):
    note = datetime.now().strftime(FORMAT)
    if say:
        SETTINGS["schedule_events"] = note
    return note


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


#
if __name__ == "__main__":
    # This is needed for automatic refresh
    schedule_events()
