from MAL_Remainder.common_utils import current_executable
from MAL_Remainder.utils import SETTINGS
from MAL_Remainder.calendar_parse import today
from datetime import datetime

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

    frame = today()
    triggers_for_end = ",".join(frame["ended"].dt.strftime("%H:%M:%S"))
    reason_for_failure = current_executable("-sch", "-triggers_for_end", triggers_for_end)

    say_we_are_done_today()
    return reason_for_failure
