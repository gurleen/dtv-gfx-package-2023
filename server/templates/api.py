import os
from pathlib import Path

from fastapi import APIRouter
from templates.template import Template
from templates.defs import TEMPLATES
from templates.graphic import Graphic
from app import DATA_PATH

router = APIRouter()

def get_video_template(fname: str) -> Template:
    without_ext = fname.split(".")[0]
    return Template(name=without_ext, template_file=f"/static/gfx/html/video.html?file={fname}", vars=[])

def get_all_videos() -> list[str]:
    for root, dirs, files in os.walk(Path(DATA_PATH, "media")):
        for name in files:
            if name.endswith(".webm"):
                yield name

@router.get("/templates")
def get_templates() -> list[Template]:
    videos = get_all_videos()
    return TEMPLATES + [get_video_template(v) for v in videos]


@router.post("/graphics")
def create_graphic(graphic: Graphic) -> Graphic:
    return graphic