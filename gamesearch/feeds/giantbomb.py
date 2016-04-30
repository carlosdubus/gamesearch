"""
    GiantBombFeed
"""
from gamesearch.feed import JsonFeed
from gamesearch.store import Game


class GiantBombFeed(JsonFeed):
    def __init__(self, api_key=None, platforms=[]):
        """
        Platforms is a list of giantbomb platforms IDs
        """
        super(GiantBombFeed, self).__init__()
        self.base_url = "http://www.giantbomb.com/api/games"
        self.default_params = {
            "api_key": api_key,
            "format": "json"
            }
        self.results_per_page = 100
        self.platforms = platforms

    def validate(self, response):
        """
        GiantBomb feed returns 1 when response is valid
        """
        return response["status_code"] == 1

    def parse(self, result):
        """
        Converts a result from GiantBomb feed into a Game objects
        """
        return Game(
            name=result.get("name"),
            description=result.get("description"),
            summary=result.get("deck"),
            platforms=[p["abbreviation"] for p in result.get("platforms", [])]
            )

    def fetch(self, platform=None):
        """
        Fetch games for a specific platform.
        It returns a generator that yields game objects
        """
        params = {
            "platforms": platform,
            "offset": 0
        }
        while(True):
            response = super(GiantBombFeed, self).fetch(params)
            for result in response["results"]:
                yield self.parse(result)
            if response["number_of_page_results"] < self.results_per_page:
                break
            params["offset"] += self.results_per_page

    def fetch_all(self, platform_list=[]):
        """
        Fetch all the games for each platform in platform_list
        """
        for platform in platform_list:
            for game in self.fetch(platform):
                yield game

    def __iter__(self):
        return self.fetch_all(self.platforms)
