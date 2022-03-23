from datetime import datetime


def get_remaining_seconds(seconds):
    expired = int(seconds - datetime.now().timestamp())
    return (expired if expired >= 0 else 0), expired < 1000


def update_now_in_seconds(x: dict):
    x["now"] = int(datetime.now().timestamp())
    return x
