import random
from flask import Flask, render_template, redirect, url_for, request, abort
import requests
import pathlib
from urllib.parse import urlparse, urljoin
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import Process, Queue, ProcessError
import webbrowser
from threading import Timer
import sys
from _thread import interrupt_main
import traceback

if __name__ == "__main__":
    from MAL_Remainder.common_utils import update_now_in_seconds, get_remaining_seconds, current_executable, EnsurePort, \
        ROOT
    from MAL_Remainder.oauth_responder import OAUTH, gen_session
    from MAL_Remainder.utils import get_headers, SETTINGS, is_there_token
    from MAL_Remainder.mal_session import MALSession
    from MAL_Remainder.calendar_parse import quick_save, schedule_events

    session = requests.Session()

app = Flask(
    "Remainder Settings"
)


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


def traceback_error():
    return _404(traceback.format_exc())


class Server:
    def __init__(self):
        self.settings = SETTINGS
        self.executor = ThreadPoolExecutor(thread_name_prefix="Remainder-Server")
        self._MAL = None
        self._MAL = self.mal_session() if is_there_token() else False
        self.OAUTH_process = None

    def mal_session(self):
        if self._MAL:
            return self._MAL

        try:
            self._MAL = MALSession(session, get_headers())
            return self.mal_session()
        except Exception as _:
            return False

    def settings_page(self):
        error = [0, ""]

        try:
            expires_in, expired = get_remaining_seconds(
                int(self.settings["expires_in"]) + int(self.settings["now"])
            )
            error[0] = expires_in

            ... if self.settings["id"] or expired else self.refresh(self.settings.to_dict())
        except ValueError:
            error[
                -1] = "Failed to check the expiry date of the refresh tokens!, Maybe we don't have your refresh token.\nGo get one!"
        except Exception as _:
            error[-1] = traceback.format_exc()

        return render_template(
            "settings.html",
            name="settings.html",
            settings=self.settings,
            profile=url_for("static", filename="Profile" + self.settings["picture"]),
            error=error[-1],
            expire_time=error[0],
        )

    def reset_settings(self):
        raw = request.form

        if "refresh" in raw:
            return self.refresh(raw)

        try:
            self.settings.from_dict(request.form, False)
            self.close_oauth()
            self.force_oauth()
            self.refresh()

        except Exception as _:
            return traceback_error()

        self.settings.connection.commit()
        return redirect("/settings")

    def refer_settings(self):
        try:
            current_executable("-ask")
            return redirect("/settings")
        except Exception as _:
            return abort(404, traceback.format_exc())

    def refresh(self, raw):
        # Refreshing Tokens...
        refresh_cal = "calendar" in raw and raw["calendar"] and raw["calendar"] != self.settings["calendar"]

        response = session.post(
            f"{OAUTH}/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.settings("refresh_token"),
                "client_id": self.settings("CLIENT_ID"),
                "client_secret": self.settings("CLIENT_SECRET"),
            },
        )
        response.raise_for_status()
        self.settings.from_dict(update_now_in_seconds(response.json()))

        # Fetching your name and profile picture
        response = session.get(self.mal_session().postfix("users", "@me"), headers=get_headers())
        response.raise_for_status()

        self.settings.from_dict(profile_pic(response.json()))

        self.refresh_events(raw["calendar"]) if refresh_cal else ...

        return redirect("./settings")

    def update_things(self):
        try:
            watch_list = list(self.mal_session().watching())
        except AttributeError:
            return abort(404,
                         "Failed to fetch your watch list! Maybe you don't have a valid token? Are you sure it's not expired\nGo to Settings to know more!")
        except Exception as error:
            return abort(404, repr(error))

        watch_list, overflown = watch_list[:-1], watch_list[-1]

        return render_template(
            "mini_board.html",
            watch_list=watch_list,
            len=len,
            reversed=reversed,
            settings=self.settings,
        )

    def refresh_events(self, url=""):
        url = url if url else self.settings["calendar"]
        if not url:
            return

        quick_save(url if url else self.settings("calendar"), False)

        failed = schedule_events(True)

        if failed:
            raise ProcessError(failed)
        else:
            self.settings["calendar"] = url

    def calendar_refresh(self):
        try:
            self.refresh_events()
        except ProcessError:
            return abort(404, "Failed to schedule events!, Here's the logs:\n" + traceback.format_exc())

        return redirect("/settings")

    def update_things_in_site(self):
        form = request.form

        self.mal_session().post_changes(
            form["animes"],
            int(form["up_until"]) + int(form["watched"]),
            int(form["total"]),
        ) if (
                form.get("watched", 0)
                and "animes" in form
                and "up_until" in form
                and "total" in form
        ) else ...

        if len(sys.argv) == 2:
            # yes, it's not good practice, but since it's not meant to be used manually, it's fine this way for now.
            interrupt_main()
            return abort(410)

        return redirect("./settings")

    def force_oauth(self):
        pipe = Queue()
        process = Process(
            target=gen_session,
            args=(
                SETTINGS("REDIRECT_HOST"),
                SETTINGS("REDIRECT_PORT"),
                SETTINGS("CLIENT_ID"),
                SETTINGS("CLIENT_SECRET"),
                pipe,
            ),
        )
        self.OAUTH_process = pipe, process

        process.start()
        process.join()

        if pipe.empty():
            raise ConnectionAbortedError(
                "Failed to contact the server, Probably the server is busy!!! try to close that")

        raw = pipe.get(block=False)
        if not raw or type(raw) == str:
            raise ConnectionRefusedError(raw)

        return SETTINGS.from_dict(raw)

    def close_oauth(self):
        if self.OAUTH_process:
            pipe, process = self.OAUTH_process
            pipe.close()
            process.terminate()
            self.OAUTH_process = None

        return redirect("./settings")

    def dep_db(self):
        print(self.settings.to_dict())

        return redirect("./settings")


def gen_url(_port):
    arguments = sys.argv[1:]
    arguments.append("automatic") if len(arguments) == 0 else ...
    route = "" if len(arguments) == 1 else arguments[-1]

    return f"http://localhost:{_port}/{route}"


if __name__ == "__main__":
    app.static_folder = str(ROOT / "static")
    app.template_folder = str(ROOT / "templates")

    SERVER = Server()

    app.add_url_rule("/settings", view_func=SERVER.settings_page)
    app.add_url_rule("/save-settings", view_func=SERVER.reset_settings, methods=["POST"])
    app.add_url_rule("/import-settings", view_func=SERVER.refer_settings)

    app.add_url_rule("/", view_func=SERVER.update_things)
    app.add_url_rule("/force-scheduler", view_func=SERVER.update_things)
    app.add_url_rule("/save-events", view_func=SERVER.calendar_refresh)

    app.add_url_rule(
        "/update-status", view_func=SERVER.update_things_in_site, methods=["POST"]
    )
    app.add_url_rule("/close-oauth_session", view_func=SERVER.close_oauth)

    app.add_url_rule("/dep-db", view_func=SERVER.dep_db)

    trust = EnsurePort("/settings", "mal-remainder")

    if trust.deep_check():
        sys.exit(0)

    port = trust()
    trust.acquire(port)

    Timer(
        random.uniform(0.69, 1),
        lambda: webbrowser.open(gen_url(port)),
    ).start()

    app.run(host="localhost", port=port, debug=False)
    trust.release()

# Reference: https://myanimelist.net/blog.php?eid=835707
