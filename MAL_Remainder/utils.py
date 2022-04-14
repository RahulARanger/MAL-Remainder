import typing
import pathlib
import sqlite3

from MAL_Remainder.common_utils import ensure_data


class Settings:
    def __init__(self, source=None):
        self.connection = sqlite3.connect(
            source if source else ensure_data().joinpath("settings.db"),
            timeout=6,
            check_same_thread=False,
        )
        self.error = False
        self.connection.executescript(
            pathlib.Path(__file__).parent.joinpath("init.sql").read_text()
        )

    def __getitem__(self, key) -> str:
        value = self.connection.execute(
            "SELECT Value from Settings where key = (?);", (key,)
        ).fetchone()
        return value[-1] if value else ""

    def __setitem__(self, key, value):
        cursor = self.connection.execute(
            "INSERT OR REPLACE INTO Settings (key, value) VALUES (?, ?);", (key, value)
        )
        self.connection.commit()
        cursor.close()

    def __delitem__(self, key):
        cursor = self.connection.execute(
            "DELETE FROM Settings WHERE key = (?);", (key,)
        )
        self.connection.commit()
        cursor.close()

    def from_dict(self, container: dict, commit: bool = True):
        cursor = self.connection.executemany(
            "INSERT OR REPLACE INTO SETTINGS (key, value) Values(?, ?);",
            {_: container[_] for _ in container if container[_]}.items(),
        )
        self.connection.commit() if commit else ...
        cursor.close()

    def to_dict(self):
        return dict(
            self.connection.execute("SELECT Key, Value FROM Settings;").fetchall()
        )

    def from_keys(self, keys: typing.List[str]):
        values = dict(
            self.connection.execute(
                "SELECT Key, Value from Settings WHERE Key in (%s);"
                % ("?," * len(keys))[:-1],
                keys,
            ).fetchall()
        )
        return values

    def __call__(self, key):
        value = self[key]

        if not value:
            raise KeyError(key)
        return value

    def close(self):
        self.connection.close()

    def get(self, key, default=""):
        store = self[key]
        if not store:
            return default
        return store

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        return False


SETTINGS = Settings()


def is_there_token():
    return SETTINGS["token_type"] and SETTINGS["access_token"] and SETTINGS["CLIENT_ID"] and SETTINGS["CLIENT_SECRET"]


def get_headers():
    raw = SETTINGS.from_keys(
        ["access_token", "expires_in", "refresh_token", "token_type"]
    )
    return {"Authorization": f'{raw["token_type"]} {raw["access_token"]}'}


class Tock:
    def __init__(self, source=ensure_data() / "tock.csv"):
        self.source = source
        self.source.touch()

    def headers(self):
        return [
            "ID", "Title", "Image", "Done", "Total", "Genre"
        ]


if __name__ == "__main__":
    check = Settings()
    print(check.to_dict())

    print(check.from_keys(["API", "NAME"]))
