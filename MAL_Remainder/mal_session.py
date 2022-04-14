import requests
from collections import namedtuple
import typing
import pathlib
import logging
from urllib.parse import urlparse


def sanity_check(response: requests.Response):
    raw = response.json()
    if raw.get("error", ""):
        raise ConnectionRefusedError(raw.get("error"))
    response.raise_for_status()
    return raw


class MALSession:
    def __init__(self, session: requests.Session, headers: typing.Callable, refresh_func: typing.Callable):
        self.api_url = "https://api.myanimelist.net/v2/"
        self.session = session
        self.headers = headers
        self.prevent = refresh_func

        self.core_info = namedtuple(
            "Anime",
            ["id", "title", "main_picture", "list_status"]
        )

    def postfix(self, fix="users", *then):
        return self.api_url + fix + "/" + "/".join(then)

    def watching(self, sort_order="list_updated_at"):
        self.prevent()
        logging.info("Fetching your watch-list")

        raw = sanity_check(self.session.get(
            self.postfix() + "@me/animelist",
            params={"status": "watching", "sort": sort_order, "fields": "list_status"},
            headers=self.headers()
        ))

        for node in raw["data"]:
            node["list_status"].update(self.total_episodes(node["node"]["id"]))
            yield self.core_info(
                **node["node"], list_status=node["list_status"]
            )
        yield bool(raw["paging"])

    def total_episodes(self, anime_id):
        self.prevent()

        logging.info("Fetching the total number of episodes for anime %s", anime_id)
        return sanity_check(self.session.get(
            self.postfix("anime", str(anime_id)), headers=self.headers(), params={
                "fields": "num_episodes,genres,rank,popularity,mean"
            }
        ))

    def post_changes(self, anime_id, watched, total):
        self.prevent()

        logging.info("Updating your preferences for anime %s with %s out of %s", anime_id, watched, total)
        return sanity_check(self.session.patch(
            self.postfix("anime", str(anime_id), "my_list_status"), headers=self.headers(),
            data={
                "num_watched_episodes": watched,
                "status": "completed" if watched == total else "watching"
            }
        ))

    def profile_pic(self, about_me):
        url = about_me["picture"]
        logging.info("Fetching your profile picture")
        save_to = (
                pathlib.Path(__file__).parent
                / "static" / "data"
                / ("Profile" + pathlib.Path(urlparse(url).path).suffix)
        )

        with save_to.open("wb") as save_as:
            response = self.session.get(url, stream=True)

            for chunk in response:
                save_as.write(chunk)

        about_me["picture"] = save_to.suffix

        return about_me

    def about_me(self):
        logging.info("Fetching details about you")
        return self.profile_pic(
            sanity_check(
                self.session.get(self.postfix("users", "@me"), headers=self.headers())
            )
        )
