from fastapi import FastAPI, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cv2
import logging
import uvicorn
import numpy as np
import io
from logic import convert_to_base64, predict
from PIL import Image

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "title": "radiologists"
    }
    return templates.TemplateResponse("home.html", {"request": request, "data": data})


@app.post("/file", response_class=HTMLResponse)
async def create_file(request: Request, file: bytes = File(...)):
    try:
        logging.info('Loading image...')

        # convert image from bytes to CV2
        image = Image.open(io.BytesIO(file))
        opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        logging.info('Successfully uploaded image')
    except Exception as e:
        msg = 'Error while uploading. Please, make sure that you are uploading an image.'
        logging.error(f'{msg}: {e}')
        return msg

    try:
        output_image = predict(opencvImage)
    except Exception as e:
        msg = 'Error during prediction...'
        logging.error(f'{msg}: {e}')
        raise e

    request_data = {
        'input_image': convert_to_base64(file),
        'output_image': convert_to_base64(output_image)
    }
    return templates.TemplateResponse("output.html", {"request": request, "data": request_data})


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
