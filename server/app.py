from pathlib import Path, PurePath
from typing import Any

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from platformdirs import *
from socketio import AsyncServer
from starlette.responses import Response
from starlette.staticfiles import StaticFiles


class NoCacheStaticFiles(StaticFiles):
    def __init__(self, *args: Any, **kwargs: Any):
        self.cachecontrol = "max-age=0, no-cache, no-store, , must-revalidate"
        self.pragma = "no-cache"
        self.expires = "0"
        super().__init__(*args, **kwargs)

    def file_response(self, *args: Any, **kwargs: Any) -> Response:
        resp = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cachecontrol)
        resp.headers.setdefault("Pragma", self.pragma)
        resp.headers.setdefault("Expires", self.expires)
        return resp


sio = AsyncServer(async_mode="asgi")
fastapi_app = FastAPI()
fastapi_app.mount(
    "/static",
    NoCacheStaticFiles(directory="./static", html=True, check_dir=True),
    name="static",
)
fastapi_app.mount(
    "/media",
    NoCacheStaticFiles(directory="./media", html=True, check_dir=True),
    name="media",
)

DATA_PATH: PurePath = Path(user_documents_dir(), "dragonstv-data")
DATA_PATH.mkdir(parents=True, exist_ok=True)
