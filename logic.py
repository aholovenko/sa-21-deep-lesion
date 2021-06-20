import base64
import io
import logging
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

from model import preprocess_image, postprocess_image

logging.basicConfig(level=logging.INFO)


def predict(opencv_image, ai_model):
    # make prediction
    model_output = predict_model(opencv_image, ai_model)

    final_image = postprocess_image(model_output, opencv_image)
    return final_image


def predict_model(img, classifier):
    logging.debug("predict lesions with DNN model")

    input_tensor = preprocess_image(img)
    output = classifier(input_tensor)

    return output


def matplotlib_viz(image):
    def fig2img(fig):
        """Convert a Matplotlib figure to a PIL Image and return it"""
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        img = Image.open(buf)
        return img

    def image_to_byte_array(image: Image):
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format=image.format)
        img_byte_array = img_byte_array.getvalue()
        return img_byte_array

    figure = plt.figure()
    plot = figure.add_subplot(111)
    plot.imshow(image)

    matplotlib_plotted_image = image_to_byte_array(fig2img(figure))
    return matplotlib_plotted_image


def ct_scan_image_to_rgb(image):
    return np.stack([image] * 3, axis=2) + 50


def convert_to_base64(obj):
    logging.debug("Convert to base64")
    base64_data = base64.b64encode(obj)  # convert to base64 as bytes
    return base64_data.decode()  # convert bytes to string
