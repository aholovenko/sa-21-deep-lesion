import unittest
import cv2
import torch

import numpy as np

from fastapi.testclient import TestClient
from http import HTTPStatus
from requests import HTTPError
from torchmetrics import IoU

from setup import (app,
                   DNN_MODEL)
from model import (ct_read,
                   preprocess_image)


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

    def test_model_prediction(self):
        img_path = "data/000007_03_01/040.png"
        mask_path = "data/000007_03_01/040.npy"

        # img_path = "data/000062_01_01/060.png"
        # mask_path = "data/000062_01_01/060.npy"

        metric = IoU(num_classes=2)
        iou_threshold = 0.4

        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        img = ct_read(img)

        mask = np.load(mask_path)
        mask = mask[:, :, 0]
        mask = torch.tensor(mask).long()
        # print(f"mask shape: {mask.shape}")
        # print(f"mask unique: {np.unique(mask)}")
        # print(mask.min(), mask.max())

        input_tensor = preprocess_image(img)
        # print(f"input shape: {input_tensor.shape}")

        pred = DNN_MODEL(input_tensor)
        pred = pred.data
        pred = pred[0][0] + pred[0][1] + pred[0][2] + pred[0][3]
        # print(pred.max(), pred.min())

        pred = pred.clip(0, 1)

        # TODO make fake prediction to check assert
        # pred = torch.rand(512, 512)

        # print(pred.max(), pred.min())
        # print(f"pred shape: {pred.shape}")
        # print(pred.dtype)

        score = metric(pred, mask)
        # print(f"score: {score}")
        assert score > iou_threshold, "Low IoU score"
