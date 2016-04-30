import json
from gamesearch.index import InvertedIndex
import os
import os.path


class GameStore:
    def __init__(self, data_dir=None):
        self.data_dir = data_dir
        self.meta_file = data_dir + "/store.meta"
        self.last_game_id = 0
        self.name_index = InvertedIndex(path=self.data_dir + "/index")
        os.makedirs(self.name_index.path, exist_ok=True)

    def save_meta(self):
        with open(self.meta_file, "w") as fp:
            json.dump({
                "last_game_id": self.last_game_id
            }, fp)

    def load_meta(self):
        if not os.path.isfile(self.meta_file):
            return
        with open(self.meta_file, "r") as fp:
            meta = json.load(fp)
            self.last_game_id = meta["last_game_id"]

    def get_game_file(self, game_id):
        return self.data_dir + "/" + str(game_id) + ".game"

    def add(self, game):
        game.id = self.last_game_id
        with open(self.get_game_file(game.id), "w") as fp:
            json.dump(game.__dict__, fp)
        self.name_index.add_document(game.name, game.id)
        self.last_game_id += 1
        self.save_meta()

    def get(self, game_id):
        with open(self.get_game_file(game_id), "r") as fp:
            return Game(**json.load(fp))

    def find_by_name(self, query):
        return [self.get(game_id) for game_id in self.name_index.query(query)]


class Game:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.summary = kwargs.get("summary")
        self.platforms = kwargs.get("platforms")


# gs = GameStore("data/games")

# # gs.add(Game(("Mario Tennis")))
# # gs.add(Game(("Mario Party 4")))
# # gs.add(Game(("Dr. Mario")))
# # gs.add(Game(("Big Party: Super Mario Fun Time")))
# # gs.add(Game(("Tetris Party")))
# # gs.save("data/games.index")
# # gs = GameStore.load("data/games.index")
# print([g.name for g in gs.find_by_name("tetris")])