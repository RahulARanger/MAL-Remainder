import requests
from collections import namedtuple


class MALSession:
    def __init__(self, session: requests.Session, headers: dict):
        self.api_url = "https://api.myanimelist.net/v2/"
        self.session = session
        self.headers = headers

        self.core_info = namedtuple(
            "Anime",
            ["id", "title", "main_picture", "list_status"]
        )

    def postfix(self, fix="users", then=""):
        return self.api_url + fix + "/" + then

    def watching(self, sort_order="list_updated_at"):
        response = self.session.get(
            self.postfix() + "@me/animelist", params={"status": "watching", "sort": sort_order, "fields": "list_status"}, headers=self.headers
        )
        response.raise_for_status()

        raw = response.json()

        for node in raw["data"]:
            node["list_status"]["num_episodes"] = self.total_episodes(node["node"]["id"])
            yield self.core_info(
                **node["node"], list_status=node["list_status"]
            )
        yield bool(raw["paging"])

    def total_episodes(self, anime_id):
        response = self.session.get(
            self.postfix("anime", str(anime_id)), headers=self.headers, params={
                "fields": "num_episodes"
            }
        )

        response.raise_for_status()

        return response.json().get("num_episodes", 0)

    def post_changes(self, anime_id, watched):
        response = self.session.patch(self.postfix("anime", str(anime_id)), headers=self.headers, data={
            "num_episodes_watched": watched
        })
        response.raise_for_status()
