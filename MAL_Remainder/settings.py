import os
import pathlib
import random
import tempfile
from flask import Flask, render_template, redirect, url_for, request, abort
import requests
from urllib.parse import urljoin
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import Process, Queue, ProcessError
import webbrowser
from threading import Timer
import sys
from _thread import interrupt_main
import traceback
import csv

if __name__ == "__main__":
    from MAL_Remainder.common_utils import update_now_in_seconds, get_remaining_seconds, EnsurePort, \
        ROOT, raise_top, current_executable
    from MAL_Remainder.oauth_responder import OAUTH, gen_session
    from MAL_Remainder.utils import get_headers, SETTINGS, is_there_token, Settings, Tock
    from MAL_Remainder.mal_session import MALSession
    from MAL_Remainder.calendar_parse import quick_save, schedule_events

    session = requests.Session()

app = Flask(
    "Remainder Settings"
)


@app.errorhandler(410)
def _410(_):
    return render_template("410.html", name="410.html"), 410


def get_absolute_route(route):
    return urljoin(request.root_url, route)


def show_exception(message):
    return webbrowser.open(urljoin(request.url_root, "404/?failed=" + message))


class ErrorPages:
    @classmethod
    @app.errorhandler(404)
    def e_404(cls):
        failed = traceback.format_exc()
        raise_top()
        return render_template(
            "error.html",
            failed=failed,
            error_code=404,
            sub_title="Most Probably this is not a valid page. If it was valid, Maybe there was error in .",
            show_settings=True
        ), 404


class Server(ErrorPages):
    def __init__(self, auto):
        self.settings = SETTINGS
        self.executor = ThreadPoolExecutor(thread_name_prefix="Remainder-Server")
        self._MAL = None
        self._MAL = self.mal_session() if is_there_token() else False
        self.OAUTH_process = None
        self.auto = auto

    def update_things(self):
        try:
            if not self.settings["name"]:
                self.update_profile()

            watch_list = list(self.mal_session().watching())
        except AttributeError:
            return abort(
                404,
                "Failed to fetch your watch list! Maybe you don't have a valid token? Are you sure it's not expired\n"
                "Go to Settings to know more!"
            )

        except Exception as _:
            return abort(404)

        watch_list, overflown = watch_list[:-1], watch_list[-1]

        return render_template(
            "mini_board.html",
            watch_list=watch_list,
            len=len,
            reversed=reversed,
            settings=self.settings,
        )

    def update_but_before_ensure(self):
        try:
            self.actually_refresh_tokens()
            self.update_profile()
        except Exception as _:
            abort(
                404, "Failed to either refresh tokens which is most probable thing to happen now or update your profile"
            )

        return redirect("/")

    def mal_session(self):
        if self._MAL:
            return self._MAL

        try:
            self._MAL = MALSession(session, get_headers, self.check_and_then_refresh_tokens)
            return self.mal_session()
        except Exception as _:
            return False

    def update_profile(self):
        # Fetching your name and profile picture
        response = session.get(self.mal_session().postfix("users", "@me"), headers=get_headers())
        response.raise_for_status()
        self.settings.from_dict(self.mal_session().profile_pic(response.json()))

    # TOKEN RELATED THINGS STARTS HERE

    def actually_refresh_tokens(self):
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

    def refresh_tokens(self):
        try:
            self.actually_refresh_tokens()
            return redirect("/settings")
        except Exception as _:
            return self.settings_page(
                "Failed to refresh tokens, Maybe your refresh tokens and access tokens are not valid. Try to ReOauth"
            )

    def check_and_then_refresh_tokens(self):
        expires_in, expired = get_remaining_seconds(
            int(self.settings["expires_in"]) + int(self.settings["now"])
        )
        self.actually_refresh_tokens() if expired else ...
        return expires_in

    # Settings Page

    def settings_page(self, failed: str = ""):
        error = [0, failed]

        try:
            error[0] = self.check_and_then_refresh_tokens()

        except ValueError:
            error[-1] = "Failed to check the expiry date of the refresh tokens!," \
                        "Maybe we don't have your refresh token.\nGo get one! "

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

    def edit_settings(self):
        raw = request.form

        if "calendar" in raw:
            try:
                self.fetch_events(raw["calendar_url"])
                return redirect("/settings")
            except ConnectionRefusedError:
                return redirect(url_for("/settings", failed="Failed to fetch calendar from the given URL"))
            except ProcessError:
                return redirect(url_for("/settings", failed="Failed to schedule events"))

        if "replace" in raw:
            return self.import_settings()

        self.settings.from_dict(raw, False)

        try:
            self.close_oauth()
            self.force_oauth()
            self.actually_refresh_tokens()
            self.update_profile()
        except Exception as _:
            print(_)
            return abort(404)

        self.settings.connection.commit()
        return redirect("/settings")

    def fetch_events(self, url=None):
        url = url if url else self.settings["calendar"]
        if not url:
            raise ConnectionRefusedError("No calendar url given")

        quick_save(url, False)

        failed = schedule_events(True)

        if failed:
            raise ProcessError(failed)
        else:
            self.settings["calendar"] = url

    def update_things_in_site(self):
        form = request.form
        print(form)

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

        if sys.argv[0] == "automatic":
            # yes, it's not good practice, but since it's not meant to be used manually, it's fine this way for now.
            return redirect("./close-session")

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

    def close_session(self):
        self.settings.close()
        Timer(0.5, lambda: interrupt_main()).start()
        return render_template(
            "error.html",
            error_code=102,
            sub_title="Session closed as requested!",
            sugestion="Please close the browser window",
            show_settings=False
        )

    def import_settings(self):
        file = request.files["settings-file"]
        if not file:
            self.settings_page("No file selected")

        _, path = tempfile.mkstemp(suffix=".db", prefix="settings")
        os.close(_)
        temp = pathlib.Path(path)
        file.save(temp)

        store = [""]
        try:
            _ = Settings(temp)
            self.settings.from_dict(_.to_dict())
            _.close()
            store[-1] = "Successfully imported settings"
        except Exception as _:
            store[-1] = "Failed to import settings"
        else:
            try:
                self.update_profile()
            except Exception as _:
                store[-1] = "Failed to update profile"
        finally:
            temp.unlink()

        return self.settings_page(store[-1])


if __name__ == "__main__":
    app.static_folder = str(ROOT / "static")
    app.template_folder = str(ROOT / "templates")

    sys.argv.append("automatic") if len(sys.argv) == 1 else ...
    sys.argv.append("") if len(sys.argv) == 2 else ...

    SERVER = Server(sys.argv[1] == "automatic")

    app.add_url_rule("/", view_func=SERVER.update_things)
    app.add_url_rule("/ensure", view_func=SERVER.update_but_before_ensure)

    app.add_url_rule("/settings", view_func=SERVER.settings_page)
    app.add_url_rule("/edit-settings", view_func=SERVER.edit_settings, methods=["POST"])
    app.add_url_rule("/refresh-tokens", view_func=SERVER.refresh_tokens)

    app.add_url_rule(
        "/update-status", view_func=SERVER.update_things_in_site, methods=["POST"]
    )
    app.add_url_rule("/close-oauth_session", view_func=SERVER.close_oauth)
    app.add_url_rule("/close-session", view_func=SERVER.close_session)

    app.add_url_rule("/test", view_func=SERVER.dep_db)

    trust = EnsurePort("/settings", "mal-remainder")

    if trust.deep_check():
        sys.exit(0)

    port = trust()
    trust.acquire(port)

    Timer(
        random.uniform(0.69, 1),
        lambda: webbrowser.open(f"http://localhost:{port}/{sys.argv[-1]}"),
    ).start()

    app.run(host="localhost", port=port, debug=False)
    trust.release()

    current_executable("-update")

# Reference: https://myanimelist.net/blog.php?eid=835707
