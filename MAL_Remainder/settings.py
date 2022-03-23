from flask import Flask, render_template, redirect, url_for, request, abort
import requests
import pathlib
from urllib.parse import urlparse, urljoin
from concurrent.futures.thread import ThreadPoolExecutor
import webbrowser

if __name__ == "__main__":
    from MAL_Remainder.utils import get_headers, SETTINGS, OAUTH

    session = requests.Session()

app = Flask("Remainder Settings")


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

        return render_template(
            "settings.html",
            name="settings.html",
            settings=self.settings,
            profile=url_for("static", filename="Profile" + self.settings["picture"]),
            error=error[-1]
        )

    def abouts(self, force=False):
        if not force and self.settings['id']:
            return

        response = session.get(
            f"{self.settings['API']}/@me", headers=get_headers()
        )
        response.raise_for_status()
        self.settings.from_dict(profile_pic(response.json()))

    def save_settings(self):
        self.settings.from_dict(request.form)
        return redirect("./settings")

    def fetch_abouts(self):
        try:
            self.abouts(True)
        except Exception as error:
            return abort(410, repr(error))
        return redirect("./settings")

    def refresh_tokens(self):
        try:
            response = session.get(f'{OAUTH}/token', data={
                "grant_type": "refresh_token",
                "refresh_token": self.settings("refresh_token")
            })
            response.raise_for_status()
            self.settings.from_dict(response.json())
        except Exception as _:
            return abort(410, repr(_))

        return redirect("./settings")


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
    app.add_url_rule("/save-settings", view_func=SERVER.save_settings, methods=["POST"])
    app.add_url_rule("/fetch-about", view_func=SERVER.fetch_abouts)
    app.add_url_rule("/refresh-tokens", view_func=SERVER.refresh_tokens)

    app.run(debug=True)
