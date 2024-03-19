import os
from pathlib import Path

import minesweeper
from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse

GITHUB_PROFILE_URL = os.environ["GITHUB_PROFILE_URL"]
BASE_PATH = Path("./resources/images/minesweeper/png/")


router = APIRouter(prefix="/ms")
game = minesweeper.Minesweeper((14, 16), 35)
flag_mode = False


@router.get("/img/{i}/{j}")
def get_board_img(i: int, j: int):
    if (i, j) in game.revealed:
        if game.board[i][j] == -1:
            return FileResponse(
                BASE_PATH / "mine_red.png",
                headers={"Cache-Control": "no-cache, max-age=0"},
            )
        return FileResponse(
            BASE_PATH / f"{game.board[i][j]}.png",
            headers={"Cache-Control": "no-cache, max-age=0"},
        )
    if game.game_over and game.board[i][j] == -1:
        return FileResponse(BASE_PATH / "mine.png", headers={"Cache-Control": "no-cache, max-age=0"})
    if (i, j) in game.flags:
        return FileResponse(BASE_PATH / "flag.png", headers={"Cache-Control": "no-cache, max-age=0"})
    return FileResponse(BASE_PATH / "closed.png", headers={"Cache-Control": "no-cache, max-age=0"})


@router.get("/img/{text}")
def get_img(text: str):
    match text:
        case "flag-toggle":
            if flag_mode:
                return FileResponse(BASE_PATH / "flag.png", headers={"Cache-Control": "no-cache, max-age=0"})
            else:
                return FileResponse(
                    BASE_PATH / "deactivated_flag.png", headers={"Cache-Control": "no-cache, max-age=0"}
                )
        case "digit1":
            return FileResponse(BASE_PATH / "dnull.png", headers={"Cache-Control": "no-cache, max-age=0"})
        case "digit2":
            return FileResponse(BASE_PATH / "d3.png", headers={"Cache-Control": "no-cache, max-age=0"})
        case "digit3":
            return FileResponse(BASE_PATH / "d5.png", headers={"Cache-Control": "no-cache, max-age=0"})
        case "header":
            return FileResponse(BASE_PATH / "header.png", headers={"Cache-Control": "no-cache, max-age=0"})
        case "undo":
            return FileResponse(BASE_PATH / "undo.png", headers={"Cache-Control": "no-cache, max-age=0"})
        case "face":
            if game.game_over:
                return FileResponse(BASE_PATH / "face_lose.png", headers={"Cache-Control": "no-cache, max-age=0"})
            else:
                return FileResponse(BASE_PATH / "face.png", headers={"Cache-Control": "no-cache, max-age=0"})
        case _:
            return 404


@router.get("/play/{i}/{j}")
def play(i: int, j: int):
    if flag_mode:
        if (i, j) in game.flags:
            game.flags.remove((i, j))
        else:
            game.add_flag(i, j)
    else:
        if (i, j) not in game.flags:
            game.play(i, j)
    return RedirectResponse(GITHUB_PROFILE_URL)


@router.get("/toggle-flag")
def flag_toggle():
    global flag_mode
    flag_mode = not flag_mode
    return RedirectResponse(GITHUB_PROFILE_URL)


@router.get("/reset")
def reset():
    global game
    game = minesweeper.Minesweeper((14, 16), 34)
    return RedirectResponse(GITHUB_PROFILE_URL)


@router.get("/undo")
def undo():
    # TODO: Implement undo
    return RedirectResponse(GITHUB_PROFILE_URL)
