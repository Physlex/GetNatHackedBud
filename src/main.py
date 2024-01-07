from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import uvicorn

from models import User
from socketManager import SocketMan

from pathlib import Path

### GLOBALS

app = FastAPI()


### API

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/static/css", StaticFiles(directory="static/css"), name="static/css")
app.mount("/static/data", StaticFiles(directory="static/data"), name="static/data")
app.mount("/static/js", StaticFiles(directory="static/js"), name="static/js")

@app.get("/", response_class=HTMLResponse)
async def index():
    path = Path("templates/index.html")
    html: str = ""
    with open(path, 'r') as file:
        html = file.read()

    return HTMLResponse(html)

@app.get("/download")
async def download():
    """
        TODO: Takes a userID and returns it's associated streamed data
    """
    userID = 0
    new_user = User(userID)
    new_user.createUser()

    new_data = [0, 0, 1]
    new_user.upload(new_data)
    data = new_user.download()

    new_user.deleteUser()
    return JSONResponse(data)

@app.post("/authenticate")
async def authenticate(userID):
    return JSONResponse(True)

@app.websocket("/connect")
async def connect(websocket: WebSocket):
    await websocket.accept()


## MAIN

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
    pass
