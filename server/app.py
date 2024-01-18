from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from socketio import AsyncServer
from platformdirs import *
from pathlib import Path, PurePath

sio = AsyncServer(async_mode="asgi")
fastapi_app = FastAPI()
fastapi_app.mount("/static", StaticFiles(directory="./static", html=True, check_dir=True), name="static")
fastapi_app.mount("/media", StaticFiles(directory="./media", html=True, check_dir=True), name="media")

DATA_PATH: PurePath = Path(user_documents_dir(), "dragonstv-data")
DATA_PATH.mkdir(parents=True, exist_ok=True)