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
        <form action="/uploadfile/" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        logging.info('Loading image...')
        image = Image.open(io.BytesIO(contents))  # TODO create class for image types - jpg, png, etc? 
        logging.info(f'Successfully uploaded image {file.filename}')
    except Exception as e:
        msg = f'Error while uploading image'
        logging.error(f'{msg}: {e}')
        return msg
    return image


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
