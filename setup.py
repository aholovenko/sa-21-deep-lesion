from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from PIL import Image
import logging
import io
import uvicorn

app = FastAPI()


@app.get('/hello')
async def say_hello():
    return {"msg": "Hello radiologists!!"}


@app.get("/")
async def main():
    content = """
        <body>
        <form action="/file/" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)


@app.post("/file/")
async def create_file(file: bytes = File(...)):
    try:
        logging.info('Loading image...')
        image = Image.open(io.BytesIO(file))  # TODO: create class for image types - jpg, png, etc? 
        logging.info(f'Successfully uploaded image')
    except Exception as e:
        msg = f'Error while uploading. Please, make sure that you are uploading an image.'
        logging.error(f'{msg}: {e}')
        return msg
    return f'Successfully upladed file of size {image.size} and format {image.format}'


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
