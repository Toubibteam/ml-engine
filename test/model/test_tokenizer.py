#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from model.tokenizer import Tokenizer

class Test(unittest.TestCase):
    """
    tokenize
    """

    """
    should tokenize a sentence
    """
    def test_tokenize_1(self):
        sentence = "j'aime nous aimons le chocolat noir préféré"

        expected = [ u"j", u"aim", u"nous", u"aimon", u"chocolat", u"noir", u"prefer" ]

        tkz = Tokenizer()

        self.assertEqual(tkz.tokenize(sentence), expected)


    """
    remove_accents
    """

    """
    should remove accents from a word
    """
    def test_remove_accents_1(self):
        word = "françois a adoré aller à la fête des pélerins"

        expected = "francois a adore aller a la fete des pelerins"

        tkz = Tokenizer()

        self.assertEqual(tkz.remove_accents(word), expected)


if __name__ == "_main__":
    unittest.main()
