from pathlib import Path
from .template import Template, TemplateVar, TemplateVarType

TEMPLATES = [
    Template(name="Talent Lower Third Single", template_file="/static/gfx/html/talent-lower-third-single.html", vars=[
        TemplateVar(name="Name", key="Name", type=TemplateVarType.STRING, default="FIRSTNAME LASTNAME"),
        TemplateVar(name="Caption", key="Caption", type=TemplateVarType.STRING, default="DRAGONSTV"),
    ]),
    Template(name="Talent Lower Third Double", template_file="/static/gfx/html/talent-lower-third-double.html", vars=[
        TemplateVar(name="Left First Name", key="Left-First-Name", type=TemplateVarType.STRING, default="FIRSTNAME"),
        TemplateVar(name="Left Last Name", key="Left-Last-Name", type=TemplateVarType.STRING, default="LASTNAME"),
        TemplateVar(name="Right First Name", key="Right-First-Name", type=TemplateVarType.STRING, default="FIRSTNAME"),
        TemplateVar(name="Right Last Name", key="Right-Last-Name", type=TemplateVarType.STRING, default="LASTNAME"),
    ]),
    Template(name="Player Lower Third Two Line", template_file="/static/gfx/html/lower-third-two-line.html", vars=[
        TemplateVar(name="Team", key="Team", type=TemplateVarType.OPTION, default="Home", choices=["Home", "Away"]),
        TemplateVar(name="Player", key="Player", type=TemplateVarType.INTEGER, default=0),
        TemplateVar(name="Top Line", key="Line-1", type=TemplateVarType.STRING, default="THE QUICK BROWN FOX JUMPS"),
        TemplateVar(name="Bottom Line", key="Line-2", type=TemplateVarType.STRING, default="OVER THE LAZY DOG"),
    ]),
    Template(name="Player Lower Third One Line", template_file="/static/gfx/html/lower-third-one-line.html", vars=[
        TemplateVar(name="Team", key="Team", type=TemplateVarType.OPTION, default="Home", choices=["Home", "Away"]),
        TemplateVar(name="Player", key="Player", type=TemplateVarType.INTEGER, default=0),
        TemplateVar(name="Line", key="Single-Line-Text", type=TemplateVarType.STRING, default="THE QUICK BROWN FOX JUMPS"),
    ]),
    Template(name="Player Lower Third Stat", template_file="/static/gfx/html/lower-third-stat.html", vars=[
        TemplateVar(name="Team", key="Team", type=TemplateVarType.OPTION, default="Home", choices=["Home", "Away"]),
        TemplateVar(name="Player", key="Player", type=TemplateVarType.INTEGER, default=0),
        TemplateVar(name="Stat Name 1", key="Stat-Name-1", type=TemplateVarType.STRING, default="FG"),
        TemplateVar(name="Stat Value 1", key="Stat-Value-1", type=TemplateVarType.STRING, default="0/0"),
        TemplateVar(name="Stat Name 2", key="Stat-Name-2", type=TemplateVarType.STRING, default="3PT"),
        TemplateVar(name="Stat Value 2", key="Stat-Value-2", type=TemplateVarType.STRING, default="0/0"),
        TemplateVar(name="Stat Name 3", key="Stat-Name-3", type=TemplateVarType.STRING, default="FT"),
        TemplateVar(name="Stat Value 3", key="Stat-Value-3", type=TemplateVarType.STRING, default="0/0"),
        TemplateVar(name="Stat Name 4", key="Stat-Name-4", type=TemplateVarType.STRING, default="PTS"),
        TemplateVar(name="Stat Value 4", key="Stat-Value-4", type=TemplateVarType.STRING, default="0"),
    ]),
    Template(name="Scorebug", template_file="/static/gfx/html/scorebug.html", vars=[
        TemplateVar(name="Home Timeouts", key="Home-Timeouts", type=TemplateVarType.INTEGER, default=4),
        TemplateVar(name="Away Timeouts", key="Away-Timeouts", type=TemplateVarType.INTEGER, default=4),
        TemplateVar(name="Home Bonus", key="show:Home-Bonus", type=TemplateVarType.BOOLEAN, default=False),
        TemplateVar(name="Away Bonus", key="show:Away-Bonus", type=TemplateVarType.BOOLEAN, default=False),
        TemplateVar(name="Period", key="Period", type=TemplateVarType.OPTION, default="1st", choices=["1st", "2nd", "3rd", "4th", "OT", "2OT", "3OT", "Final"]),
        TemplateVar(name="Slider Color", key="sliderColor", type=TemplateVarType.OPTION, default="neutral", choices=["neutral", "home", "away"]),
        TemplateVar(name="Info-Bar-Title", key="Info-Bar-Title", type=TemplateVarType.STRING, default=""),
        TemplateVar(name="Info-Bar-Caption", key="Info-Bar-Caption", type=TemplateVarType.STRING, default=""),
        TemplateVar(name="Info Bar Trigger", key="scorebugSlider", type=TemplateVarType.BUTTON, default=""),
    ]),
    Template(name="Matchup", template_file="/static/gfx/html/Matchup/Matchup.html", vars=[]),
    Template(name="Big Scoreboard", template_file="/static/gfx/html/Big Scoreboard/Big Scoreboard.html", vars=[
        TemplateVar(name="Period", key="Period", type=TemplateVarType.STRING, default=""),
    ]),
    Template(name="Starting Five", template_file="/static/gfx/html/starting-five.html", vars=[
        TemplateVar(name="Team", key="Team", type=TemplateVarType.OPTION, default="Home", choices=["Home", "Away"]),
        TemplateVar(name="Players", key="Players", type=TemplateVarType.STRING, default=""),
    ]),
    Template(name="Halftime Stats", template_file="/static/gfx/html/halftime-stats.html", vars=[
        TemplateVar(name="Home Stats (csv)", key="Home-Stats", type=TemplateVarType.STRING, default=""),
        TemplateVar(name="Away Stats (csv)", key="Away-Stats", type=TemplateVarType.STRING, default=""),
        TemplateVar(name="Home Score", key="Home-Score", type=TemplateVarType.STRING, default=""),
        TemplateVar(name="Away Score", key="Away-Score", type=TemplateVarType.STRING, default=""),
    ]),
    Template(name="Halftime Stats - Auto", template_file="/static/gfx/html/halftime-stats.html", vars=[
        TemplateVar(name="ESPN (mbb) or NCAA (wbb) Game ID", key="Game-ID", type=TemplateVarType.STRING, default=""),
    ]),
    Template(name="CAA Standings", template_file="/static/gfx/html/caa-standings.html", vars=[
        TemplateVar(name="Gender", key="gender", type=TemplateVarType.OPTION, choices=["mens", "womens"], default="mens")]
    )
]