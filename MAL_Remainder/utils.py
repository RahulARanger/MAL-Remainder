import typing
import pathlib
import sqlite3

from MAL_Remainder.oauth_responder import gen_session, OAUTH
from multiprocessing import Process, Queue


class Settings:
    def __init__(self):
        self.connection = sqlite3.connect(
            pathlib.Path(__file__).parent / "settings.db", timeout=6, check_same_thread=False
        )
        self.connection.execute("BEGIN EXCLUSIVE");
        self.connection.executescript(pathlib.Path(__file__).parent.joinpath("init.sql").read_text())

    def __getitem__(self, key) -> str:
        value = self.connection.execute("SELECT Value from Settings where key = (?);", (key,)).fetchone()
        return value[-1] if value else ""

    def __setitem__(self, key, value):
        cursor = self.connection.execute("INSERT OR REPLACE INTO Settings (key, value) VALUES (?, ?);", (key, value))
        self.connection.commit()
        cursor.close()

    def __delitem__(self, key):
        cursor = self.connection.execute("DELETE FROM Settings WHERE key = (?);", (key,))
        self.connection.commit()
        cursor.close()

    def from_dict(self, container: dict):
        cursor = self.connection.executemany("INSERT OR REPLACE INTO SETTINGS (key, value) Values(?, ?);",
                                             container.items())
        self.connection.commit()
        cursor.close()

    def to_dict(self):
        return dict(self.connection.execute("SELECT Key, Value FROM Settings;").fetchall())

    def from_keys(self, keys: typing.List[str]):
        values = dict(self.connection.execute(
            "SELECT Key, Value from Settings WHERE Key in (%s);" % ("?," * len(keys))[:-1], keys).fetchall())
        return values

    def __call__(self, key):
        value = self[key]

        if not value:
            raise KeyError(key)
        return value

    def close(self):
        self.connection.close()


SETTINGS = Settings()


def get_raw_tokens():
    return SETTINGS.from_keys(["access_token", "expires_in", "refresh_token", "token_type"])


def ask_tokens(f):
    def rly_ask():
        pipe = Queue()
        process = Process(target=gen_session,
                          args=(SETTINGS("REDIRECT_HOST"), SETTINGS("REDIRECT_PORT"), SETTINGS("CLIENT_ID"),
                                SETTINGS("CLIENT_SECRET"), pipe))
        process.start()
        process.join()

        if pipe.empty():
            raise ConnectionAbortedError("Failed to authenticate for fetching tokens")

        raw = pipe.get(block=False)

        if not raw or type(raw) == str:
            raise ConnectionRefusedError(raw)

        return SETTINGS.from_dict(raw)

    def internal_work(*_, **__):
        try:
            return f(*_, **__)
        except Exception as ___:
            rly_ask()
            return f(*_, **__)

    return internal_work


@ask_tokens
def get_token():
    raw = get_raw_tokens()
    return f'{raw["token_type"]} {raw["access_token"]}'


def get_headers():
    return {"Authorization": get_token()}


if __name__ == "__main__":
    check = Settings()
    print(check.to_dict())

    print(check.from_keys(["API", "NAME"]))
