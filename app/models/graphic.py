import msgspec
from typing import Literal


class Field(msgspec.Struct):
    name: str
    field_type: Literal["text", "color", "image"]
    value: str


class Graphic(msgspec.Struct):
    name: str
    svg_path: str
    fields: list[Field]