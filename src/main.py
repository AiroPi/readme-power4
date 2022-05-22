import os

from connect4 import Connect4
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, RedirectResponse

from .connect4_image_generator import generate_image

app = FastAPI()
c4 = Connect4()
if not os.path.exists("./data/"):
    os.mkdir("./data/")
generate_image(c4, "./data/connect4.png")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/image")
def get_image():
    return FileResponse("./data/connect4.png", headers={"Cache-Control": "no-cache, max-age=0"})


@app.get("/play")
def play(
    column: int = Query(title="The column ID you want to play to.", ge=0, le=6)
):
    c4.play(column)
    generate_image(c4, "./data/connect4.png")
    return RedirectResponse("https://gist.github.com/AiroPi/ae65bc8ca2a44ff8c286d18630a4c3dd")
