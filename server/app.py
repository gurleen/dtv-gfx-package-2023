from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from socketio import AsyncServer

sio = AsyncServer(async_mode="asgi")
fastapi_app = FastAPI()
fastapi_app.mount("/static", StaticFiles(directory="../static", html=True), name="static")
fastapi_app.mount("/media", StaticFiles(directory="../media", html=True), name="media")