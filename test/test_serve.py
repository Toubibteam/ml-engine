import unittest
import serve

class Test(unittest.TestCase):
    def test__to_json(self):
        expected = {
            "code_id": "code_id",
            "metric": "metric",
            "description": "description"
        }

        self.assertEqual(serve._to_json("code_id", "metric", "description"), expected)

if __name__ == "_main__":
    unittest.main()
