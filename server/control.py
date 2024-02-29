from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/control")
def control_page():
    return FileResponse("static/control/index.html")


@router.get("/control/basketball")
def basketball_control():
    return FileResponse("static/control/basketball/index.html")