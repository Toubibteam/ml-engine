import pandas as pd
from collections import Counter


from config import UNK


class Vocab(object):
    """Class to handle tokens <-> preprocessing <-> ids"""

    def __init__(self, filename):
        self._filename = filename
        self.load_vocab()


    def load_vocab(self):
        special_tokens = [UNK]
        self._tok_to_id = load_tok_to_id(self._filename, special_tokens)
        self._id_to_tok = {idx: tok for tok, idx in self._tok_to_id.iteritems()}
        self.n_tok = len(self._tok_to_id)
        self.id_unk = self._tok_to_id[UNK]


    def tok_to_id(self, tok):
        return self._tok_to_id[tok] if tok in self._tok_to_id else self.id_unk


    def id_to_tok(self, _id):
        return self._id_to_tok[_id]


def build_vocab(code_dataset, min_count=1):
    """Build vocab from dataset"""
    print("Building vocab...")
    c = Counter()
    for code_id, description,type_ in code_dataset:
        c.update(description)
    vocab = [tok for tok, count in c.items() if count >= min_count]
    print("- done. {}/{} tokens added to vocab.".format(len(vocab), len(c)))
    return sorted(vocab)


def write_vocab(vocab, filename):
    """Writes one word per line.

    Args:
        vocab: iterable that yields word
        filename: path to vocab file

    Returns:
        write a word per line

    """
    print("Writing vocab...")
    with open(filename, "w") as f:
        for i, word in enumerate(vocab):
            if i != len(vocab) - 1:
                f.write("{}\n".format(word.encode('utf-8')))
            else:
                f.write(word.encode('utf-8'))
    print("- done. {} tokens".format(i+1))


def load_tok_to_id(filename, tokens=[]):
    """
    Args:
        filename: (string) path to vocab txt file one word per line
        tokens: list of token to add to vocab after reading filename

    Returns:
        dict: d[token] = id

    """
    tok_to_id = dict()
    with open(filename) as f:
        for idx, token in enumerate(f):
            token = token.strip()
            tok_to_id[token] = idx

    # add extra tokens
    for tok in tokens:
        tok_to_id[tok] = len(tok_to_id)

    return tok_to_id
