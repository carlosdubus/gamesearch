import pickle


class GameStore:
    def __init__(self):
        self.meta_file = None
        self.dir = None
        self.last_game_id = 0

    def save_meta(self):
        with open(self.meta_file, "wb") as fp:
            pickle.dump(self, fp)

    def get_game_file(self, game_id):
        return self.dir + "/" + str(game_id) + ".game"

    def add(self, game):
        with open(self.get_game_file(self.last_game_id), "wb") as fp:
            pickle.dump(game, fp)
        self.last_game_id += 1

    def get(self, game_id):
        with open(self.get_game_file(game_id), "rb") as fp:
            return pickle.load(fp)

    def ingest(self, feed):
        """
        Ingests a feed
        """
        for game in iter(feed):
            self.add(game)

    @staticmethod
    def load(filename):
        with open(filename, "rb") as fp:
            return pickle.load(fp)


class Game:
    def __init__(self):
        self.name = None
        self.description = None
        self.summary = None
