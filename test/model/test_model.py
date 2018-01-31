import unittest
from model.model import Model

class Test(unittest.TestCase):
    # @classmethod
    # def setUpModule(cls):
    #     cls._model = Model("CCAM")


    def test_similarity(self):
        query = "this this is a short sentence".split()
        description = "this is something else".split()

        expected = 2
        self.assertEqual(Model.similarity(query, description), expected)


    def test_description_representation(self):
        description = "this is something else"

        expected = "this is something else"
        self.assertEqual(Model.description_representation(description), expected)


if __name__ == "_main__":
    unittest.main()
