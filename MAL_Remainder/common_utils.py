import subprocess
import pathlib
from sqlite3 import connect
import webbrowser
import socket
import logging
from threading import Timer
from _thread import interrupt_main

ROOT = pathlib.Path(__file__).parent


def ensure_data():
    data = ROOT / "static" / "data"
    data.mkdir(exist_ok=True)

    return data


def close_main_thread_in_good_way(wait=0.9):
    return Timer(wait, lambda: interrupt_main()).start()


def get_local_url(port):
    return f"http://localhost:{port}/"


def open_local_url(port, wait=1, postfix=""):
    return Timer(wait, lambda: webbrowser.open(get_local_url(port) + postfix)).start()


class EnsurePort:
    @classmethod
    def get_free_port(cls):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("localhost", 0))
            port = sock.getsockname()[1]
            return port

    def __init__(self, fall_back, file_name_prefix):
        self.root = ensure_data() / (file_name_prefix + "ports.db")
        self.conn = None
        self.fall_back = "http://localhost:"
        self.revive()
        self.fall_back = (
            f"{self.fall_back}{self.get_port()}{fall_back}" if self.fall_back else ""
        )

    def get_port(self):
        cursor = self.conn.execute("SELECT * FROM ports")
        port = cursor.fetchone()
        cursor.close()
        return port[-1] if port else None

    def acquire(self, port):
        cursor = self.conn.execute("INSERT INTO ports VALUES (?)", (port,))
        self.conn.commit()
        cursor.close()

    def locked(self):
        if not self.fall_back:
            return False
        return self.get_port() is not None

    def deep_check(self):
        if not self.locked():
            return False

        self.conn.close()

        try:
            self.root.unlink(missing_ok=True)
        except PermissionError:
            webbrowser.open(self.fall_back) if self.fall_back else ...
            return True

        self.revive()
        return False

    def revive(self):
        # it's clear that its unlocked
        self.fall_back = self.fall_back if self.root.exists() else ""

        self.conn = connect(self.root)
        self.conn.executescript(
            self.root.parent.parent.parent.joinpath("lock_script.sql").read_text()
        )

    def release(self):
        self.conn.close()
        del self.conn
        return self.root.unlink()


def current_executable(*args):
    logging.info("Calling shell with %s", args)

    temp = subprocess.run(
        ["setup", *args],
        capture_output=True,
        shell=True,
        check=True,
        cwd=pathlib.Path(__file__).parent.parent
    )
    logging.info(temp.stdout.decode())


def ask_for_update():
    subprocess.Popen(
        ["setup", "-update"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=pathlib.Path(__file__).parent.parent,
        start_new_session=True
    )


def get_cols():
    return [
        "ID",
        "Title",
        "Image",
        "Done",
        "Watched",
        "Total",
        "Genre",
        "Score",
        "Rank",
        "Popularity Rank",
        "Today"
    ]


def get_raw_file():
    file = ensure_data() / "data.csv"
    file.exists() or file.write_text(",".join(get_cols()) + "\n")
    file.touch()
    return file


if __name__ == "__main__":
    current_executable("-help")
