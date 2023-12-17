from typing import Any, Optional, Union
from pydantic import BaseModel, validator
from strenum import StrEnum
from enum import auto


class TemplateVarType(StrEnum):
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    IMAGE = auto()
    COLOR = auto()
    OPTION = auto()
    BOOLEAN = auto()
    BUTTON = auto()


class TemplateVar(BaseModel):
    name: str
    key: str
    type: TemplateVarType
    default: Union[str, int, float]
    image_dir: Optional[str] = None
    value: Optional[Any] = None
    choices: Optional[list[str]] = None

    @validator("image_dir", always=True)
    def check_image_dir(cls, v, values):
        if values["type"] == TemplateVarType.IMAGE:
            assert (
                v is not None
            ), "Image directory must be provided for image template variables"
        return v

    @validator("default", always=True)
    def check_default(cls, v, values):
        if values["type"] == TemplateVarType.INTEGER:
            assert isinstance(v, int), "Default value must be an integer"
        elif values["type"] == TemplateVarType.FLOAT:
            assert isinstance(v, float), "Default value must be a float"
        return v


class Template(BaseModel):
    id: Optional[str] = None
    name: str
    template_file: str
    vars: list[TemplateVar]