from fastapi import APIRouter
from templates.template import Template
from templates.defs import TEMPLATES
from templates.graphic import Graphic

router = APIRouter()

@router.get("/templates")
def get_templates() -> list[Template]:
    return TEMPLATES


@router.post("/graphics")
def create_graphic(graphic: Graphic) -> Graphic:
    return graphic