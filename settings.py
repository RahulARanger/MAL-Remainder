from flask import Flask, render_template, redirect
import os
import requests
import pathlib
import json
import subprocess
import sys
from datetime import timedelta
from urllib.parse import urlparse

API_URL = "https://api.myanimelist.net/v2/users"
session = requests.Session()
app = Flask("Remainder Settings")


def get_raw_tokens():
    tokens = pathlib.Path(__file__).parent / "tokens.json"
    ... if tokens.exists() else tokens.write_text("{}")

    return json.load(tokens.open())


def ask_tokens(f):
    def rly_ask():
        process = subprocess.Popen(
            [sys.executable, pathlib.Path(__file__).parent / "oauth_responder.py"]
        )
        try:
            process.wait(timeout=timedelta(minutes=3).total_seconds())
        except Exception as _:
            print("Failed to ask for the tokens", _)
            ...
            sys.exit(-1)

    def internal_work(*_, **__):
        try:
            return f(*_, **__)
        except Exception as ___:
            rly_ask()
            return f(*_, **__)

    return internal_work


def profile_pic(abouts: dict):
    url = abouts.get("picture", "")
    if not url:
        return

    save_to = (
        pathlib.Path(__file__).parent
        / "Media"
        / ("Profile" + pathlib.Path(urlparse(url).path).suffix)
    )

    with save_to.open("wb") as save_as:
        response = session.get(url, stream=True)

        for chunk in response:
            save_as.write(chunk)


@ask_tokens
def get_token():
    raw = get_raw_tokens()
    assert raw, "No tokens available"
    return f'{raw["token_type"]} {raw["access_token"]}'


def get_headers():
    return {"Authorization": get_token()}


def abouts(force=False):
    abouts = pathlib.Path(__file__).parent / "abouts.json"
    ask = not force or abouts.exists()

    ... if abouts.exists() else abouts.write_text("{}")
    loaded = json.load(abouts.open())

    if not ask:
        return loaded

    try:
        response = session.get(
            "https://api.myanimelist.net/v2/users/@me", headers=get_headers()
        )

        response.raise_for_status()
        abouts.write_text(json.dumps(response.json(), indent=4))
        profile_pic(response.json())
        loaded["failed"] = False

    except requests.exceptions.ConnectionError:
        loaded["failed"] = "network problem (DNS failure, refused connection, etc)"
    except Exception as e:
        loaded["failed"] = repr(e)

    return loaded


@app.route("/")
def home():
    about_me = abouts()
    return render_template(
        "settings.html", name="settings.html", os=os, about_me=about_me
    )


@app.route("/fetch_about")
def fetch_abouts():
    abouts(force=True)
    return redirect("/")


@app.route("/schedule")
def show_schedule():
    ...


app.run(debug=True)
