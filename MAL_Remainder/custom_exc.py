import traceback
import logging

import requests
from multiprocessing import ProcessError


class ExcHandler:
    def __init__(self, kwargs):
        self.unsafe = ""
        self.expected_errors = {**kwargs}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if not exc_type:
            return

        self.unsafe = self.expected_errors[exc_type] if self.expected_errors.get(exc_type, "") else (
                "\n" + "".join(traceback.format_tb(exc_tb))
        )
        self.unsafe += f"\n\n{exc_type}\n{exc_value}"
        logging.exception(exc_value, exc_info=True)
        return True


def connection_related_exc(kwargs=None):
    kwargs = kwargs if kwargs else {}
    return ExcHandler(
        {
            ConnectionRefusedError: "Server refused to connect! Maybe invalid credits or tokens?"
                                    "Either way Server refused because of incorrect information",
            requests.ConnectionError: "Connection Error! Has to do with your internet connection mostly",
            requests.HTTPError: "HTTP Error! Hmm maybe you are trying to access a page that doesn't exist",
            **kwargs
        }
    )


def calendar_exc():
    return ExcHandler({
        ConnectionRefusedError: "Refused to Connect because of missing URL or connection related issue",
        requests.ConnectionError: "Failed to connect to make a request due to connection",
        requests.HTTPError: "Invalid Calendar URL",
        ProcessError: "Failed to Schedule Events, Maybe powershell guy didn't cooperate with us"
    })
