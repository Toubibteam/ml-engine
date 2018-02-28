from collections import Counter

from config import UNK

class Vocab(object):
    """ Class to handle the conversion between tokens and ids """

    def __init__(self, filename):
        self.load_vocab(filename)


    def load_vocab(self, filename):
        """ Load vocabulary from a text file and convert tokens to ids

        Args:
            self: (object) the class instance
            filename: (string) path to the file containing the list of tokens

        Returns:
            none

        """
        special_tokens = [UNK]
        self.tok_to_id_dict = load_tok_to_id(filename, special_tokens)
        self.id_to_tok_dict = {idx: tok for tok, idx in self.tok_to_id_dict.iteritems()}
        self.n_tok = len(self.tok_to_id_dict)
        self.id_unk = self.tok_to_id_dict[UNK]


    def tok_to_id(self, tok):
        """ Convert a token to an id

        Args:
            self: (object) the class instance
            tok: (string) the token to convert

        Returns:
            (string) id

        """
        return self.tok_to_id_dict[tok] if tok in self.tok_to_id_dict else self.id_unk


    def id_to_tok(self, id):
        """ Convert an id to a token

        Args:
            self: (object) the class instance
            id: (string) the id to convert

        Returns:
            (string) token

        """
        return self.id_to_tok_dict[id]


def build_vocab(code_dataset, min_count=1):
    """Build vocab from dataset"""
    print("Building vocab...")
    c = Counter()
    for code_id, description in code_dataset:
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


def load_tok_to_id(filename, special_tokens=[]):
    """
    Args:
        filename: (string) path to vocab txt file one word per line
        special_tokens: (list) tokens to add to vocab after reading filename

    Returns:
        dict: d[token] = id

    """
    tok_to_id = dict()
    with open(filename) as f:
        for idx, t in enumerate(f):
            tok_to_id[t.strip()] = idx

    # add extra tokens
    nbIds = len(tok_to_id)
    for idx, tok in enumerate(special_tokens):
        tok_to_id[tok] = nbIds + idx

    return tok_to_id
