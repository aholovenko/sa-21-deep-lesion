from fastapi.testclient import TestClient
from http import HTTPStatus
from setup import app
import unittest
import os


class TestApplication(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_file_upload(self):
        response = self.client.post('/file', data={'file': open('images/test-ct-scan.jpg', 'rb')})
        assert response.status_code == HTTPStatus.OK
        assert response.content != b'"Error while uploading. Please, make sure that you are uploading an image."'
