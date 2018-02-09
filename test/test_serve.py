import unittest
import serve

class Test(unittest.TestCase):
    def test__to_json(self):
        expected = {
            "code_id": "code_id",
            "metric": "metric",
            "description": "description",
            "tarif": "tarif"
        }

        self.assertEqual(serve._to_json("code_id", "metric", "description","tarif"), expected)

if __name__ == "_main__":
    unittest.main()
