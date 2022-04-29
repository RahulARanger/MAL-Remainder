import os
import pathlib
import random
import tempfile
from flask import Flask, render_template, redirect, url_for, request, abort
import requests
from urllib.parse import urlencode
from multiprocessing import Process, Queue
import sys
import traceback
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    from MAL_Remainder import __version__
    from MAL_Remainder.common_utils import EnsurePort, \
        ROOT, raise_top, ask_for_update, close_main_thread_in_good_way, open_local_url
    from MAL_Remainder.oauth_responder import OAUTH, gen_session
    from MAL_Remainder.utils import get_headers, SETTINGS, is_there_token, Settings, write_row, get_remaining_seconds
    from MAL_Remainder.mal_session import MALSession, sanity_check
    from MAL_Remainder.calendar_parse import quick_save, schedule_events, stamp, update_now_in_seconds
    from MAL_Remainder.custom_exc import connection_related_exc, calendar_exc

    session = requests.Session()

app = Flask(
    "Remainder Settings"
)


@app.errorhandler(410)
def _410(_):
    return render_template(
        "error.html",
        failed=_,
        error_code=410,
        show_settings=True,
        sub_title="Please refer the below message",
        suggestion=_
    ), 410


class ErrorPages:
    @classmethod
    @app.errorhandler(404)
    def e_404(cls):
        # logging.exception("Internal Exception", exc_info=True, stack_info=True)
        failed = traceback.format_exc()
        raise_top()
        return render_template(
            "error.html",
            failed=failed,
            error_code=404,
            sub_title="Not a Valid Route!",
            suggestion="Mal-Remainder only has few valid routes,like /settings, /force-remainder, /.",
            show_settings=True
        ), 404

    @classmethod
    def call_settings_with_error(cls, msg):
        return redirect("/settings?" + urlencode({"failed": msg}))


class Server(ErrorPages):
    def __init__(self, auto):
        self.settings = SETTINGS
        self._MAL = None
        self._MAL = self.mal_session() if is_there_token() else False
        self.OAUTH_process = None
        self.auto = auto
        self.confirmed = self.settings.get("auto-update", "0") == "1"

    def update_things(self):
        logging.info("Opening Mini-DashBoard")

        with connection_related_exc() as exc:
            if not self.settings["name"]:
                self.update_profile()

            watch_list = list(self.mal_session().watching())
            logging.info("Ready with Watch List")

        if exc.unsafe:
            return abort(410, exc.unsafe)

        watch_list, overflown = watch_list[:-1], watch_list[-1]

        return render_template(
            "mini_board.html",
            watch_list=watch_list,
            len=len,
            reversed=reversed,
            settings=self.settings,
        )

    def update_but_before_ensure(self):
        logging.info("proceeding in a safe way before redirecting to mini dashboard")

        with connection_related_exc() as exc:
            self.actually_refresh_tokens()
            self.update_profile()

        if exc.unsafe:
            abort(410, exc.unsafe)

        return redirect("/")

    def mal_session(self):
        if self._MAL:
            return self._MAL

        if not is_there_token():
            raise ConnectionRefusedError(
                "Failed to get required Credentials for contacting MAL Server"
                ". Make Sure to fill Client ID, Client Secret, access_token, refresh_token"
            )

        self._MAL = MALSession(session, get_headers, self.check_and_then_refresh_tokens)
        return self.mal_session()

    def update_profile(self):
        self.settings.from_dict(
            self.mal_session().about_me()
        )

    # TOKEN RELATED THINGS STARTS HERE

    def actually_refresh_tokens(self):
        logging.info("Asking to refresh the access tokens")
        self.settings.from_dict(update_now_in_seconds(sanity_check(
            session.post(
                f"{OAUTH}/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.settings("refresh_token"),
                    "client_id": self.settings("CLIENT_ID"),
                    "client_secret": self.settings("CLIENT_SECRET"),
                },
            ))))

    def check_and_then_refresh_tokens(self, force=False):
        expires_in, expired = get_remaining_seconds()
        self.actually_refresh_tokens() if force or expired else ...
        return expires_in

    # Settings Page

    def settings_page(self):
        # Automatic mode is off
        logging.info("Rendering Settings Page...")
        error_message = request.args.get("failed", "")
        expiry_time: int = 0
        expiry_time -= 0  # just to avoid type hint
        self.auto = False

        with connection_related_exc(
                {ValueError: "Invalid or Missing Tokens! Please try to Reset OAuth or feed missing values"}
        ) as exc:
            expiry_time = self.check_and_then_refresh_tokens(request.args.get("force-refresh", False, type=bool))

        if exc.unsafe:
            error_message += "\n" + exc.unsafe

        # if you face Operational Error, then you must really raise an Issue
        logging.error(error_message) if error_message else ...

        return render_template(
            "settings.html",
            name="settings.html",
            settings=self.settings,
            profile=url_for("static", filename="/Data/Profile" + self.settings["picture"]),
            error=error_message,
            expire_time=expiry_time,
            version=__version__
        )

    def edit_settings(self):
        raw = request.form

        logging.info("Requested to edit settings into")
        logging.info(raw)

        if "calendar" in raw:
            logging.info("Precisely requested for calendar things")

            with calendar_exc() as exc:
                self.fetch_events(raw["calendar_url"])
                exc.unsafe = "Rescheduled Events!"

            return ErrorPages.call_settings_with_error(exc.unsafe)

        if "replace" in raw:
            logging.info("Importing Settings")
            logging.warning(
                "Are you sure, if your client tokens or refresh tokens are valid!"
                "Importing doesn't check them.Know the status by Resetting the Oauth if normal Operations fails."
            )
            with connection_related_exc() as exc:
                exc.unsafe = self.import_settings()
            return ErrorPages.call_settings_with_error(exc.unsafe)

        self.settings.from_dict(raw, False)

        with connection_related_exc() as exc:
            self.close_oauth()
            self.force_oauth()
            self.actually_refresh_tokens()
            self.update_profile()

        if exc.unsafe:
            return ErrorPages.call_settings_with_error(exc.unsafe)

        self.settings.connection.commit()
        return redirect("/settings")

    def fetch_events(self, url=None):
        url = url if url else self.settings["calendar"]
        if not url:
            raise ConnectionRefusedError("No calendar url given")

        logging.info("Fetching events from %s", url)
        quick_save(url)

        schedule_events()
        self.settings["calendar"] = url

    def update_things_in_site(self):
        form = request.form

        with connection_related_exc() as exc:
            posted = (
                    form.get("watched", 0)
                    and "animes" in form
                    and "up_until" in form
                    and "total" in form
            )

            self.mal_session().post_changes(
                form["animes"],
                int(form["up_until"]) + int(form["watched"]),
                int(form["total"]),
            ) if posted else ...

            write_row(
                form["animes"],
                form["name"],
                form["image"],
                form["up_until"],
                form["watched"],
                form["total"],
                form["genres"],
                form["score"],
                form["rank"],
                form["popularity"],
                stamp()
            ) if posted else ...

        return abort(410, exc.unsafe) if exc.unsafe else redirect("/close-session" if self.auto else "/settings")

    def force_oauth(self):
        logging.info("Starting OAuth Session")

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
            logging.warning("Killing the Currently Running OAuth Session! Please avoid violence.")
            pipe, process = self.OAUTH_process
            pipe.close()
            process.terminate()
            self.OAUTH_process = None

        return redirect("/settings")

    def dep_db(self):
        print(self.settings.to_dict())
        raise_top()
        return redirect("/settings")

    def close_session(self):
        self.confirmed = self.settings.get("auto-update", "0") == "1"
        self.settings.close()

        close_main_thread_in_good_way()
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
            raise FileNotFoundError("Sent Empty File")

        _, path = tempfile.mkstemp(suffix=".db", prefix="settings")
        os.close(_)
        temp = pathlib.Path(path)
        file.save(temp)

        with connection_related_exc() as exc:
            with Settings(temp) as _:
                self.settings.from_dict(_.to_dict())
                exc.unsafe = "Successfully imported settings"
                print(exc.unsafe, "here")

        temp.unlink()
        self.fresh_load()

        return exc.unsafe

    def auto_update(self):
        logging.info("Toggling the auto-update status")
        self.settings["auto-update"] = "auto-update" in request.form
        return redirect('/settings')

    def fresh_load(self):
        self.update_profile()
        self.fetch_events() if self.settings["calendar"] else ...


if __name__ == "__main__":
    app.static_folder = str(ROOT / "static")
    app.template_folder = str(ROOT / "templates")

    sys.argv.append("automatic") if len(sys.argv) == 1 else ...
    sys.argv.append("") if len(sys.argv) == 2 else ...

    SERVER = Server(sys.argv[1].startswith("auto"))

    app.add_url_rule("/", view_func=SERVER.update_things)
    app.add_url_rule("/ensure", view_func=SERVER.update_but_before_ensure)

    app.add_url_rule("/settings/<failed>/<force_refresh>", view_func=SERVER.settings_page)
    app.add_url_rule("/settings", view_func=SERVER.settings_page)
    app.add_url_rule("/edit-settings", view_func=SERVER.edit_settings, methods=["POST"])

    app.add_url_rule(
        "/update-status", view_func=SERVER.update_things_in_site, methods=["POST"]
    )
    app.add_url_rule("/auto-update", view_func=SERVER.auto_update, methods=["POST"])

    app.add_url_rule("/close-oauth_session", view_func=SERVER.close_oauth)
    app.add_url_rule("/close-session", view_func=SERVER.close_session)

    app.add_url_rule("/test", view_func=SERVER.dep_db)

    trust = EnsurePort("/settings", "mal-remainder")

    if trust.deep_check():
        sys.exit(0)  # interrupt_main is good when flask is running else sys.exit

    port = EnsurePort.get_free_port()
    trust.acquire(port)

    open_local_url(port, random.uniform(0.69, 1), postfix=sys.argv[-1])

    app.run(host="localhost", port=port, debug=False)

    trust.release()

    ask_for_update() if SERVER.confirmed else ...

# Reference: https://myanimelist.net/blog.php?eid=835707
