from datetime import datetime
import pathlib
from sqlite3 import connect
import webbrowser
import socket


def get_remaining_seconds(seconds):
    expired = int(seconds - datetime.now().timestamp())
    return (expired if expired >= 0 else 0), expired < 1000


def update_now_in_seconds(x: dict):
    x["now"] = int(datetime.now().timestamp())
    return x


def ensure_data():
    data = pathlib.Path(__file__).parent / "data"
    data.mkdir(exist_ok=True)

    return data


# we can't have 2 EnsurePorts, since we only made 1 ports.db
class EnsurePort:
    def __init__(self, fall_back):
        self.root = ensure_data().parent / "ports.db"
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
            self.root.parent.joinpath("lock_script.sql").read_text()
        )

    def __call__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("localhost", 0))
            port = sock.getsockname()[1]
            return port

    def release(self):
        self.conn.close()
        del self.conn
        return self.root.unlink()
