from fastapi.testclient import TestClient
from http import HTTPStatus
from setup import app
import unittest
from requests import HTTPError


class TestApplication(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_file_upload(self):
        response = self.client.post('/file', data={'file': open('images/test-ct-scan.jpg', 'rb')})
        if response.status_code != HTTPStatus.OK:
            raise HTTPError("HTTP status code is not 200")
        if response.content == b'"Error while uploading. Please, make sure that you are uploading an image."':
            raise HTTPError("HTTP response content error")
