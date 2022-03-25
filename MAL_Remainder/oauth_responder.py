import random
import requests
from flask import Flask, request, redirect
from threading import Timer
from _thread import interrupt_main
import webbrowser
from MAL_Remainder.common_utils import update_now_in_seconds
import socket
from datetime import timedelta
from queue import Queue


def ensure_port(host, port):
    """
    Closes the Script if port found
    :param host: host in which the server should run
    :param port: port in which server should communicate
    :return: free or not
    """

    # Reference: https://stackoverflow.com/a/51094879/12318454
    if not (host or port):
        return False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
            # TESTED only on Windows
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)

        try:
            sock.bind((socket.gethostbyname(host), int(port)))
            return True
        except OSError:
            print("Already running ...")
            ...
        except Exception as _:
            ...
        return False


OAUTH = "https://myanimelist.net/v1/oauth2"


def get_new_code_verifier() -> str:
    # WARNING: didn't work for all random letters
    # will look into this later
    return "A" * 128


# https://www.oauth.com/oauth2-servers/making-authenticated-requests/refreshing-an-access-token/
class Session:
    def __init__(self, client_id, client_secret):
        self.code_challenge = get_new_code_verifier()
        self.session_state = "I LOVE REM"
        self.tokens = {}
        self.client_things = client_id, client_secret
        self.failed = None

    # Reference from https://myanimelist.net/blog.php?eid=835707
    def authorize(self):
        return redirect(
            f"{OAUTH}/authorize?response_type=code&client_id={self.client_things[0]}&code_challenge={self.code_challenge}&state={self.session_state}")

    def redirect_uri(self):
        raw = request.args
        if raw.get("state") != self.session_state:
            return "404 error"
        if "error" in raw:
            return self.close(raw.get("message"))
        return self.ask_and_save(raw.get("code"))

    def ask_and_save(self, code):
        response = requests.post(
            f"{OAUTH}/token",
            data={
                "grant_type": "authorization_code",
                "client_id": self.client_things[0],
                "client_secret": self.client_things[-1],
                "code": code,
                "code_verifier": self.code_challenge
            }
        )

        try:
            response.raise_for_status()
            self.tokens = update_now_in_seconds(response.json())
        except Exception as e:
            return self.close(repr(e))
        return self.close()

    def close(self, msg=""):
        self.failed = msg
        interrupt_main()
        return "you may now close this window"


def _gen_session(host, port, client_id, client_secret):
    assert ensure_port(host, port), "%s is already hosted in %s" % (port, host)

    app = Flask("MyAnimeList Session For Watcher")

    req_session = Session(client_id, client_secret)

    app.add_url_rule("/", view_func=req_session.authorize)
    app.add_url_rule("/save", view_func=req_session.redirect_uri)

    timers = [Timer(
        timedelta(days=0, minutes=6, seconds=0, hours=0).total_seconds(), lambda: req_session.close("Time out error")
        # waits for the 10 minutes
    )]
    timers[-1].start()

    timers.append(Timer(
        timedelta(days=0, minutes=0, seconds=random.uniform(1, 2), hours=0).total_seconds(),
        lambda: webbrowser.open(f"http://{host}:{port}/")
    ))

    timers[-1].start()

    app.run(port=port, host=host, debug=False)

    [
        _.cancel() for _ in timers if _.is_alive()
    ]

    return req_session.failed if req_session.failed else req_session.tokens


def gen_session(host, port, client_id, client_secret, queue: Queue):
    return queue.put(_gen_session(host, port, client_id, client_secret))


if __name__ == "__main__":
    gen_session("localhost", 6969, "", "", Queue())
