"""
    gamesearch.index
"""
import re
import json
import os.path


class PListRecord:
    def __init__(self, doc_id, pos):
        self.doc_id = doc_id
        self.pos = pos


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

    def intersect(self, plist1, plist2):
        result = []
        p1 = next(plist1, None)
        p2 = next(plist2, None)
        while p1 and p2:
            if p1.doc_id == p2.doc_id:
                result.append(p1)
                p1 = next(plist1, None)
                p2 = next(plist2, None)
            elif p1.doc_id < p2.doc_id:
                p1 = next(plist1, None)
            else:
                p2 = next(plist2, None)
        return result

    def query(self, query):
        tokens = self.tokenize(query)
        if not tokens:
            return []
        result = self.read_token(tokens.pop(0))
        while len(tokens) > 0:
            plist = self.read_token(tokens.pop(0))
            result = self.intersect(iter(result), plist)
        return list([p.doc_id for p in result])

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
                yield PListRecord(int(r[0]), int(r[1]))

    def add_document(self, text, doc_id):
        tokens = self.tokenize(text)
        for pos, token in enumerate(tokens):
            self.write_token(token, (doc_id, pos))
