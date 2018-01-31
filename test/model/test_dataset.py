#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import model.dataset as dataset

class Test(unittest.TestCase):
    """
    simple_tok
    """

    """
    for a non empty sentence, should return an array containing each word cleaned from accent and punctuation
    """
    def test_simple_tok(self):
        sentence = "J'ai toujours adoré le chocolat noir !".decode('utf-8')

        expected = [ "J'ai", "toujours", "adore", "le", "chocolat", "noir" ]

        self.assertEqual(dataset.simple_tok(sentence), expected)


    """
    for a None sentence, should return None
    """
    def test_simple_tok_2(self):
        sentence = None

        self.assertIsNone(dataset.simple_tok(sentence))


if __name__ == "_main__":
    unittest.main()
