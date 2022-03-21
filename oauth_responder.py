import random
import requests
from dotenv import load_dotenv
import os
import sys
from flask import Flask, request, redirect
import json
import pathlib
import socket
from threading import Timer
from _thread import interrupt_main
from datetime import timedelta
import webbrowser
import logging


logger = logging.getLogger("InternalOauth")
logger.setLevel(logging.DEBUG)


load_dotenv(pathlib.Path(__file__).parent / '.env')


def check_for_active_session():
    # Reference: https://stackoverflow.com/a/51094879/12318454
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
        # TESTED only on Windows
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)

    try:
        sock.bind((socket.gethostbyname(os.getenv('REDIRECT_HOST')), int(os.getenv('REDIRECT_PORT'))))
    except OSError:
        print("Already running ...")
        sys.exit(0)
    except Exception as _:
        print("WHAT !!!", _)
        sys.exit(-1)


check_for_active_session()
del check_for_active_session

app = Flask("MyAnimeList Session For Watcher")


timers = [Timer(
    timedelta(days=0, minutes=10, seconds=0, hours=0).total_seconds(), interrupt_main  # waits for the 10 minutes
)]
timers[-1].start()


def close():
    timers.append(Timer(timedelta(seconds=random.uniform(1, 1.5)).total_seconds(), interrupt_main))
    timers[-1].start()


def get_new_code_verifier() -> str:
    # WARNING: didn't work for all random letters
    # will look into this later
    return "A" * 128


# https://www.oauth.com/oauth2-servers/making-authenticated-requests/refreshing-an-access-token/
class Session:
    def __init__(self):
        self.code_challenge = get_new_code_verifier()
        self.session_state = "I LOVE REM"
        self.tokens = pathlib.Path(__file__).parent / "tokens.json"

    # Reference from https://myanimelist.net/blog.php?eid=835707
    def authorize(self):
        return redirect(
            f"{os.getenv('OAUTH')}/authorize?response_type=code&client_id={os.getenv('CLIENT_ID')}&code_challenge={self.code_challenge}&state={self.session_state}")

    def redirect_uri(self):
        raw = request.args
        if raw.get("state") != self.session_state:
            return "404 error"
        return self.ask_and_save(raw.get("code"))

    def ask_and_save(self, code):
        response = requests.post(
            f"{os.getenv('OAUTH')}/token",
            data={
                "grant_type": "authorization_code",
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CLIENT_SECRET"),
                "code": code,
                "code_verifier": self.code_challenge
            }
        )
        close()

        self.tokens.write_text(json.dumps(response.json(), indent=4))
        return "You may now close this!"

    def expired_check(self):
        ...

    def show_failed(self):
        ...


req_session = Session()
app.add_url_rule("/", view_func=req_session.authorize)
app.add_url_rule("/expired", view_func=req_session.expired_check)
app.add_url_rule("/save", view_func=req_session.redirect_uri)
app.add_url_rule("/failed", view_func=req_session.show_failed)

timers.append(Timer(
    timedelta(days=0, minutes=0, seconds=random.uniform(1, 2), hours=0).total_seconds(),
    lambda: webbrowser.open(f"http://{os.getenv('REDIRECT_HOST')}:{os.getenv('REDIRECT_PORT')}/")
))

timers[-1].start()

app.run(port=os.getenv("REDIRECT_PORT"), host=os.getenv("REDIRECT_HOST"), debug=False)

[
    _.cancel() for _ in timers if _.is_alive()
]
