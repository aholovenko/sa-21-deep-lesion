"""Module for DNN model operations"""
import os
import segmentation_models_pytorch as smp
import torch
import flash
import gdown
import cv2
import numpy as np
import matplotlib.pyplot as plt


def download_weights():
    url = 'https://drive.google.com/uc?id=1LzlKsVgAxldv_cHDFtPBZeRcovqkul8W'
    output_file = 'model.ckpt'
    output_path = 'static'
    file_path = os.path.join(output_path, output_file)

    if not os.path.exists(file_path):
        print('Downloading model weights...')
        gdown.download(url, file_path, quiet=False)


def preprocess_image(opencv_image):
    if opencv_image.shape != (512, 512):
        opencv_image = cv2.resize(opencv_image, (512, 512))

    image = np.expand_dims(opencv_image, axis=-1)

    preprocessed_image_as_tensor = torch.from_numpy(np.transpose(image, (2, 0, 1)).astype('float32'))
    preprocessed_image_as_tensor = preprocessed_image_as_tensor.unsqueeze(0)
    return preprocessed_image_as_tensor


def postprocess_image(output_tensor, original_input_image):
    score_map = output_tensor.data
    postprocessed_image = (original_input_image + 50)
    postprocessed_image = np.stack([postprocessed_image] * 3, axis=2)

    score_map = score_map[0][0] + score_map[0][1] + score_map[0][2] + score_map[0][3]

    postprocessed_image[:, :, 0] = np.add(postprocessed_image[:, :, 0], score_map)

    return postprocessed_image


def initialize_neural_network():
    download_weights()

    model = smp.Unet('efficientnet-b2', in_channels=1, classes=4, activation=None)
    classifier = flash.Task(model)
    checkpoint = torch.load(
        "static/model.ckpt",
        map_location=torch.device('cpu'))
    classifier.load_state_dict(checkpoint['state_dict'])
    return classifier


def ct_read(input_img: np.array, min_v=-500, max_v=600):
    # TODO: ask DICOM window range (-500, 600) from user for each particular ct-scan
    ct_scan = input_img.astype(np.float32) - 32768
    ct_scan = np.clip((ct_scan - min_v) / max_v, 0, 1) - 50
    return ct_scan


if __name__ == "__main__":
    dnn = initialize_neural_network()

    IMG_PATH = "data/000062_01_01/075.png"

    img = cv2.imread(IMG_PATH, cv2.IMREAD_UNCHANGED)
    img = ct_read(img)

    input_tensor = preprocess_image(img)

    output = dnn(input_tensor)

    result = postprocess_image(output, img)

    plt.imshow(result)
    plt.show()
