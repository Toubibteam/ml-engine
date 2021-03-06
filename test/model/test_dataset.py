#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import model.dataset as dataset
from model.config import UNK

class Test(unittest.TestCase):
    """
    formatCCAMCode
    """

    """
    for a ccam code from database, should return a formated ccam code
    """
    def test_formatCCAMCode(self):
        code = {
            "code": "A001",
            "descriptions": [
                "description 1",
                "description 2",
                "description 3"
            ],
            "parent": None
        }

        expectedKey = "A001"
        expectedValue = {
            "descriptions": [
                "description 1",
                "description 2",
                "description 3"
            ],
            "parent": None
        }

        key, value = dataset.CodeDataset.formatCCAMCode(code)

        self.assertEqual(key, expectedKey)
        self.assertEqual(value, expectedValue)


    """
    formatCIMCode
    """

    """
    for a cim code from database, should return a formated ccam code
    """
    def test_formatCIMCode(self):
        code = {
            "code": "A001",
            "descriptions": [
                "description 1",
                "description 2",
                "description 3"
            ],
            "chapter_nb": "1"
        }

        expectedKey = "A001"
        expectedValue = {
            "descriptions": [
                "description 1",
                "description 2",
                "description 3"
            ],
            "chapter_nb": "1"
        }

        key, value = dataset.CodeDataset.formatCIMCode(code)

        self.assertEqual(key, expectedKey)
        self.assertEqual(value, expectedValue)


if __name__ == "_main__":
    unittest.main()
