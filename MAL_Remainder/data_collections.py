from csv import DictWriter
from MAL_Remainder.common_utils import ensure_data
from MAL_Remainder.calendar_parse import stamp


# we have two data files
# one is about the animes that you have watched
# another is about the episodes that we have watched


def raw_file(name):
    file = ensure_data().joinpath(name)
    exists = file.exists()

    # file.touch()
    return file, exists


def from_list(body, keys):
    return {
        _: body[_] for _ in keys
    }


def check_keys(body, keys):
    return all(_ in body for _ in keys)


def write_a_row(raw, name):
    _handle, already_created = raw_file(name)

    with _handle.open("a", newline="") as handle:
        writer = DictWriter(handle, raw.keys())
        ... if already_created else writer.writeheader()
        writer.writerow(raw)


def write_from_form(form):
    pairs = from_list(
        form, [
            "id", "name", "up_until", "watched", "total", "genres", "rating", "score", "rank", "popularity", "duration"
        ]
    )
    pairs["updated"] = stamp()

    return write_a_row(
        pairs,
        "data.csv"
    )


def check_form(form):
    return form.get("watched", 0) and check_keys(form, ["up_until", "total"])


def update_details(form):
    return form["id"], form.get("watched", 0) + form["up_until"], form["total"]
