import unittest
import requests
import json
from app import app


class TestGoTravel(unittest.TestCase):
    baseURL = "http://127.0.0.1:5050"

    def test_get_recommend(self):
        response = requests.get(self.baseURL + "/recommend")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode()), {
            "status": "success", "response": "test recommend"})


if __name__ == "__main__":
    unittest.main()
