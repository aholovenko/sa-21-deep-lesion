import unittest
from fastapi.testclient import TestClient

from setup import app


class TestApplication(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_read_main(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}
