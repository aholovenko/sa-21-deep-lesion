from fastapi import FastAPI, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import cv2
import logging
import uvicorn
import numpy as np
from logic import convert_to_base64, predict, ct_scan_image_to_rgb, matplotlib_viz
from model import initialize_neural_network, ct_read

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DNN_MODEL = initialize_neural_network()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "title": "radiologists"
    }
    return templates.TemplateResponse("home.html", {"request": request, "data": data})


@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse('404.html', {'request': request})
    else:
        # Generic error page
        return templates.TemplateResponse('home.html', {
            'request': request,
            'detail': exc.detail
        })


@app.post("/file", response_class=HTMLResponse)
async def create_file(request: Request, file: bytes = File(...)):
    try:
        logging.info('Loading image...')
        if len(file) == 0:
            raise FileNotFoundError("No file was uploaded from UI or the file is empty.")

        # use numpy to construct an array from bytes
        arr = np.frombuffer(file, dtype="uint8")

        # decode the array into an image
        opencvImage = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
        opencvImage = ct_read(opencvImage)

        logging.info(f'Successfully uploaded CT-scan')
    except Exception as e:
        msg = 'Error while uploading. Please, make sure that you are uploading a CT-scan.'
        logging.error(f'{msg}: {e}')
        return msg

    try:
        output_image = predict(opencvImage, DNN_MODEL)
    except Exception as e:
        msg = 'Error during prediction...'
        logging.error(f'{msg}: {e}')
        return msg

    request_data = {
        'input_image': convert_to_base64(matplotlib_viz(ct_scan_image_to_rgb(opencvImage))),
        'output_image': convert_to_base64(matplotlib_viz(output_image))
    }
    return templates.TemplateResponse("output.html", {"request": request, "data": request_data})


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
