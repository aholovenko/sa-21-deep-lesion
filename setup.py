from fastapi import FastAPI

import uvicorn

app = FastAPI()


@app.get('/')
async def say_hello():
    return {"msg": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
