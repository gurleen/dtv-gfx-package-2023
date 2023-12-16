from socketio import ASGIApp
from app import sio, fastapi_app
import socket_handlers
import replicant
from templates.api import router as templates_router
from rosters import router as rosters_router
from fastapi.middleware.cors import CORSMiddleware

app = ASGIApp(sio, fastapi_app)
fastapi_app.include_router(templates_router)
fastapi_app.include_router(rosters_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)