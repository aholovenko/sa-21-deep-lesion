import base64
import io
import logging
import cv2

from PIL import Image

logging.basicConfig(level=logging.DEBUG)


def predict(opencvImage):
    # make prediction
    bbox_result = predict_bbox(opencvImage)
    final_image = plot_bbox_onto_image(opencvImage, bbox_result)

    # convert CV2 to PIL
    final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
    final_image = Image.fromarray(final_image)

    # convert to file-like data
    obj = io.BytesIO()  # file in memory to save image without using disk  #
    final_image.save(obj, format='png')  # save in file (BytesIO)
    obj.seek(0)

    return obj.read()


def predict_bbox(img):
    logging.debug("predict bbox")
    # TODO: add real pytorch model prediction
    return [10, 10, 100, 100]


def plot_bbox_onto_image(img, bbox):
    logging.debug("plot bbox")
    x1, y1, x2, y2 = bbox

    # Red color in BGR
    color = (0, 0, 255)

    # Line thickness of 2 px
    thickness = 2

    image_with_bbox = cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    return image_with_bbox


def convert_to_base64(obj):
    logging.debug("Convert to base64")
    base64_data = base64.b64encode(obj)  # convert to base64 as bytes
    return base64_data.decode()  # convert bytes to string
