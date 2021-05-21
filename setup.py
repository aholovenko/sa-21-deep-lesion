from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from PIL import Image
import logging
import io
import base64
import uvicorn
import cv2
import numpy as np

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get('/hello')
async def say_hello():
    return {"msg": "Hello radiologists!!"}


@app.get("/")
async def main():
    content = """
        <body>
            <form action="/file/" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept="image/png,image/jpg,image/jpeg">
                <input type="submit">
            </form>
        </body>
    """
    return HTMLResponse(content=content)


def predict(img):
    # TODO: add real pytorch model prediction
    return [10, 10, 100, 100]


def plot_bbox_onto_image(img, bbox):
    x1, y1, x2, y2 = bbox

    # Red color in BGR
    color = (0, 0, 255)

    # Line thickness of 2 px
    thickness = 2

    image_with_bbox = cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    return image_with_bbox


@app.post("/file/")
async def create_file(file: bytes = File(...)):
    try:
        logging.info('Loading image...')

        # convert image from bytes to CV2
        image_array = np.fromstring(file, np.uint8)
        opencvImage = cv2.cvtColor(np.array(image_array), cv2.COLOR_RGB2BGR)

        logging.info(f'Successfully uploaded image')
    except Exception as e:
        msg = 'Error while uploading. Please, make sure that you are uploading an image.'
        logging.error(f'{msg}: {e}')
        return msg

    # make prediction
    bbox_resut = predict(opencvImage)
    final_image = plot_bbox_onto_image(opencvImage, bbox_resut)

    # convert CV2 to PIL
    final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
    final_image = Image.fromarray(final_image)

    # convert to file-like data
    obj = io.BytesIO()  # file in memory to save image without using disk  #
    final_image.save(obj, format='png')  # save in file (BytesIO)
    obj.seek(0)

    # convert to bases64
    data = obj.read()  # get data from file (BytesIO)
    data = base64.b64encode(data)  # convert to base64 as bytes
    data = data.decode()  # convert bytes to string

    # convert to <img> with embed image
    content = f"""
            <body>
            <img style="width:400px;height:400px;" src="data:image/png;base64,{data}">
            </body>
            </div>
        """

    return HTMLResponse(content=content)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
