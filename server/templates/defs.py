from pathlib import Path
from .template import Template, TemplateVar, TemplateVarType


TEMPLATES = [
    Template(name="Talent Lower Third Single", template_file="/static/gfx/html/talent-lower-third-single.html", vars=[
        TemplateVar(name="Name", key="Name", type=TemplateVarType.STRING, default="FIRSTNAME LASTNAME"),
        TemplateVar(name="Caption", key="Caption", type=TemplateVarType.STRING, default="DRAGONSTV"),
    ]),
    Template(name="Player Lower Third Two Line", template_file="/static/gfx/html/lower-third-two-line.html", vars=[
        TemplateVar(name="Team", key="Team", type=TemplateVarType.OPTION, default="Home", choices=["Home", "Away"]),
        TemplateVar(name="Player", key="Player", type=TemplateVarType.INTEGER, default=0),
        TemplateVar(name="Top Line", key="Line-1", type=TemplateVarType.STRING, default="THQ QUICK BROWN FOX JUMPS"),
        TemplateVar(name="Bottom Line", key="Line-2", type=TemplateVarType.STRING, default="OVER THE LAZY DOG"),
    ]),
    Template(name="Scorebug", template_file="/static/gfx/html/scorebug.html", vars=[
        TemplateVar(name="Home Timeouts", key="Home-Timeouts", type=TemplateVarType.INTEGER, default=4),
        TemplateVar(name="Away Timeouts", key="Away-Timeouts", type=TemplateVarType.INTEGER, default=4),
        TemplateVar(name="Home Bonus", key="show:Home-Bonus", type=TemplateVarType.BOOLEAN, default=False),
        TemplateVar(name="Away Bonus", key="show:Away-Bonus", type=TemplateVarType.BOOLEAN, default=False),
        TemplateVar(name="Period", key="Period", type=TemplateVarType.OPTION, default="1st", choices=["1st", "2nd", "3rd", "4th", "OT", "2OT", "3OT", "Final"]),
    ]),
    Template(name="Matchup", template_file="/static/gfx/html/Matchup/Matchup.html", vars=[])
]