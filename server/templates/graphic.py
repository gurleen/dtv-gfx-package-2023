from pydantic import BaseModel, validator
from .template import Template
from .defs import TEMPLATES


class Graphic(BaseModel):
    name: str
    template_name: str
    vars: dict[str, str]
    _template: Template = None

    @property
    def template(self) -> Template:
        if self._template is None:
            self._template = self._get_template(self.template_name)
        return self._template
    
    @classmethod
    def _get_template(cls, name: str) -> Template:
        for template in TEMPLATES:
            print(template.name, name)
            if template.name == name:
                return template

    @validator("template_name", always=True)
    def check_template_name(cls, v, values):
        assert any(x.name == v for x in TEMPLATES)

    @validator("vars", always=True)
    def check_vars(cls, v, values):
        print(values)
        for var in cls._get_template(values["template_name"]).vars:
            assert var.key in v, f"Missing variable: {var.key}"
            if var.type == "INTEGER":
                assert v[var.key].isnumeric(), f"Variable {var.key} must be an integer"
            elif var.type == "FLOAT":
                assert v[var.key].replace(".", "", 1).isnumeric(), f"Variable {var.key} must be a float"
            else:
                assert isinstance(v[var.key], str), f"Variable {var.key} must be a string"
        return v