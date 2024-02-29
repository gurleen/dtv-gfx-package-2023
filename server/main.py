from socketio import ASGIApp
from app import sio, fastapi_app
import socket_handlers
import replicant
from templates.api import router as templates_router
from rosters import router as rosters_router
from control import router as control_router
from fastapi.middleware.cors import CORSMiddleware

app = ASGIApp(sio, fastapi_app)
fastapi_app.include_router(templates_router)
fastapi_app.include_router(rosters_router)
fastapi_app.include_router(control_router)
fastapi_app.include_router(socket_handlers.router)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)