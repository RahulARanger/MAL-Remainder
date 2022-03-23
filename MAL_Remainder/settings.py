from flask import Flask, render_template, redirect, url_for, request, abort
import requests
import pathlib
from urllib.parse import urlparse, urljoin
from concurrent.futures.thread import ThreadPoolExecutor
import webbrowser
from threading import Lock

if __name__ == "__main__":
    from MAL_Remainder.token_update import update_now_in_seconds, get_remaining_seconds
    from MAL_Remainder.utils import get_headers, SETTINGS, OAUTH, force_oauth

    session = requests.Session()

app = Flask("Remainder Settings")
SETTINGS_LOCK = Lock()


def ensure_settings(f):
    def ensure(*args, **kwargs):
        if SETTINGS_LOCK.locked():
            return abort(410, "Settings Lock is already Locked")

        with SETTINGS_LOCK:
            return f(*args, **kwargs)

    return ensure


def profile_pic(about_me: dict):
    url = about_me["picture"]

    save_to = (
            pathlib.Path(__file__).parent
            / "static"
            / ("Profile" + pathlib.Path(urlparse(url).path).suffix)
    )

    with save_to.open("wb") as save_as:
        response = session.get(url, stream=True)

        for chunk in response:
            save_as.write(chunk)

    about_me["picture"] = save_to.suffix

    return about_me


@app.errorhandler(404)
@app.route("/404/<failed>")
def _404(failed="Error: 404, No Page Found"):
    return render_template("404.html", name="404.html", failed=failed), 404


@app.errorhandler(410)
def _410(_):
    return render_template("410.html", name="410.html"), 410


def get_absolute_route(route):
    return urljoin(request.root_url, route)


def show_exception(message):
    return webbrowser.open(urljoin(request.url_root, "404/?failed=" + message))


class Server:
    def __init__(self):
        self.settings = SETTINGS
        self.executor = ThreadPoolExecutor(thread_name_prefix="Remainder-Server")

    def settings_page(self):
        error = [""]

        try:
            self.abouts()
        except Exception as _:
            error[-1] = repr(_)

        expires_in, expired = get_remaining_seconds(int(self.settings["expires_in"]) + int(self.settings["now"]))
        return render_template(
            "settings.html",
            name="settings.html",
            settings=self.settings,
            profile=url_for("static", filename="Profile" + self.settings["picture"]),
            error=error[-1],
            expire_time=expires_in
        )

    def abouts(self, force=False):
        if not force and self.settings['id']:
            return

        response = session.get(
            f"{self.settings['API']}/@me", headers=get_headers()
        )
        response.raise_for_status()
        self.settings.from_dict(profile_pic(response.json()))

    @ensure_settings
    def save_settings(self):
        self.settings.from_dict(request.form)
        return redirect("./settings")

    @ensure_settings
    def reset_settings(self):
        try:
            force_oauth()
            return redirect("./settings")
        except Exception as _:
            return abort(404, repr(_))

    @ensure_settings
    def fetch_abouts(self):
        try:
            self.abouts(True)
        except Exception as error:
            return abort(404, repr(error))
        return redirect("./settings")

    @ensure_settings
    def refresh_tokens(self):
        try:
            response = session.post(f'{OAUTH}/token', data={
                "grant_type": "refresh_token",
                "refresh_token": self.settings("refresh_token"),
                "client_id": self.settings("CLIENT_ID"),
                "client_secret": self.settings("CLIENT_SECRET")
            })
            response.raise_for_status()
            self.settings.from_dict(update_now_in_seconds(response.json()))

        except Exception as _:
            return abort(404, repr(_))

        return redirect("./settings")

    def show_schedule(self):
        dash.layout = self.sch.html_marked_up()
        return ...

    def force_oauth(self):
        return self.reset_settings()

    def fetch_fresh_tokens(self):
        return self.refresh_tokens()

    def re_fetch_abouts(self):
        return self.fetch_abouts()


def get_watching_order(sort_order="list_updated_at"):
    response = session.get(f"{API_URL}/@me/animelist", params={
        "status": "watching",
        "sort": sort_order
    })

    try:
        response.raise_for_status()
    except Exception as e:
        return repr(e)

    return response.json()


if __name__ == "__main__":
    SERVER = Server()

    app.add_url_rule("/settings", view_func=SERVER.settings_page)
    app.add_url_rule("/save-settings", view_func=SERVER.force_oauth, methods=["POST"])
    app.add_url_rule("/fetch_about", view_func=SERVER.re_fetch_abouts, methods=["POST"])
    app.add_url_rule("/refresh_tokens", view_func=SERVER.fetch_fresh_tokens, methods=["POST"])
    app.add_url_rule("/schedules", view_func=SERVER.show_schedule)

    app.run(debug=True)

# Reference: https://myanimelist.net/blog.php?eid=835707
