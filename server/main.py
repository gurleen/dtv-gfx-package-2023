from socketio import ASGIApp
from app import sio, fastapi_app
import socket_handlers
import replicant
from templates.api import router as templates_router
from rosters import router as rosters_router

app = ASGIApp(sio, fastapi_app)
fastapi_app.include_router(templates_router)
fastapi_app.include_router(rosters_router)