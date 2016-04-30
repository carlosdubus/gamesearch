"""
    gamesearch.index
"""
import re
import json
import os.path


class InvertedIndex:
    """
    File based inverted index

    Each game name is split into tokens, each token contains a list of (game_ids, position) tuples.
    Each token is a different file saved in self.path directory.
    The inverted index is file based, so it does not require to hold anything in memory.
    """
    def __init__(self, path=None):
        self.path = path

    def tokenize(self, text):
        return [s.lower() for s in re.split('\W+', text) if len(s) >= 2]

    def query(self, query):
        sets = []
        for token in self.tokenize(query):
            docs = list(self.read_token(token))
            sets.append(set([d[0] for d in docs]))
        return set.intersection(*sets)

    def write_token(self, token, hit):
        if not token:
            return
        with open(self.path + "/" + token, "a") as fp:
            fp.write("%s,%s,\n" % hit)

    def read_token(self, token):
        token_path = self.path + "/" + token
        if not os.path.isfile(token_path):
            return
        with open(token_path, "r") as fp:
            for line in fp:
                r = line.split(",")
                yield (r[0], r[1])

    def add_document(self, text, doc_id):
        tokens = self.tokenize(text)
        for pos, token in enumerate(tokens):
            self.write_token(token, (doc_id, pos))
