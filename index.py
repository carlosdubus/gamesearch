import re
import pprint
import json


def tokenize(text):
    return [s.lower() for s in re.split('\W+', text)]


class InvertedIndex:
    def __init__(self):
        self.token2docid = {}
        self.docid2doc = {}
        self.doc_id = 0

    def save(self, filename):
        with open(filename, 'w') as fp:
            fp.write(json.dumps(self.token2docid))
            fp.write("\n")

    def query(self, query):
        sets = []
        for token in tokenize(query):
            docs = self.query_token(token)
            sets.append(set([d[0] for d in docs]))
        return [self.docid2doc[docid] for docid in set.intersection(*sets)]

    def query_token(self, token):
        return self.token2docid[token] if token in self.token2docid else []

    def add_document(self, text, doc=None):
        if not doc:
            doc = text
        tokens = tokenize(text)
        for pos, token in enumerate(tokens):
            self.token2docid.setdefault(token, [])
            self.token2docid[token].append((self.doc_id, pos))

        self.docid2doc[self.doc_id] = doc
        self.doc_id += 1


# i = InvertedIndex()
# i.add_document("Mario Tennis")
# i.add_document("Mario Party 4")
# i.add_document("Dr. Mario")
# i.add_document("Big Party: Super Mario Fun Time")
# i.add_document("Tetris Party")
# i.save("games.index")
# print(i.query("party"))