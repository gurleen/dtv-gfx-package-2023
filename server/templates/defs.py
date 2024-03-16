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
        TemplateVar(name="Last Name Font Size", key="font:text-7", type=TemplateVarType.INTEGER, default=65),
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
    Template(name="Lower Third One Line - Manual", template_file="/static/gfx/html/lower-third-one-line.html", vars=[
        TemplateVar(name="Team", key="Team", type=TemplateVarType.OPTION, default="Home", choices=["Home", "Away"]),
        TemplateVar(name="Line", key="Single-Line-Text", type=TemplateVarType.STRING, default="THE QUICK BROWN FOX JUMPS"),
        TemplateVar(name="First Name", key="First-Name", type=TemplateVarType.STRING, default="DREXEL"),
        TemplateVar(name="Last Name", key="Last-Name", type=TemplateVarType.STRING, default="DRAGONS"),
        TemplateVar(name="Position", key="Position", type=TemplateVarType.STRING, default=""),
    ]),
    Template(name="Scorebug", template_file="/static/gfx/html/scorebug-old.html", vars=[
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
    Template(name="Scorebug v2", template_file="/static/gfx/html/scorebug-v2.html", vars=[
        TemplateVar(name="Comparison Slider Toggle", key="Comparison-Slider:toggle", type=TemplateVarType.BUTTON, default=""),
        TemplateVar(name="Home Timeouts", key="Home-Timeouts", type=TemplateVarType.INTEGER, default=4),
        TemplateVar(name="Away Timeouts", key="Away-Timeouts", type=TemplateVarType.INTEGER, default=4),
        TemplateVar(name="Home Bonus", key="show:Home-Bonus", type=TemplateVarType.BOOLEAN, default=False),
        TemplateVar(name="Away Bonus", key="show:Away-Bonus", type=TemplateVarType.BOOLEAN, default=False),
        TemplateVar(name="Period", key="Period", type=TemplateVarType.OPTION, default="1st", choices=["1st", "2nd", "3rd", "4th", "OT", "2OT", "3OT", "Final"]),
    ]),
    Template(name="Matchup", template_file="/static/gfx/html/Matchup/Matchup.html", vars=[
        TemplateVar(name="Home School Record", key="Home-School-Record", type=TemplateVarType.STRING, default=" "),
        TemplateVar(name="Away School Record", key="Away-School-Record", type=TemplateVarType.STRING, default=" "),
    ]),
    Template(name="Wrestling Matchup", template_file="/static/gfx/html/Wrestling Matchup/Wrestling Matchup.html", vars=[]),
    Template(name="Lacrosse Matchup", template_file="/static/gfx/html/Lacrosse Matchup/Lacrosse Matchup.html", vars=[]),
    Template(name="Big Scoreboard", template_file="/static/gfx/html/Big Scoreboard/Big Scoreboard.html", vars=[
        TemplateVar(name="Period", key="Period-Full", type=TemplateVarType.STRING, default=""),
    ]),
    Template(name="Starting Five", template_file="/static/gfx/html/starting-five.html", vars=[
        TemplateVar(name="Team", key="Team", type=TemplateVarType.OPTION, default="Home", choices=["Home", "Away"]),
        TemplateVar(name="Players", key="Players", type=TemplateVarType.STRING, default=""),
        TemplateVar(name="Player 1 Last Name Font Size", key="Player-1-Last-Name-Font-Size", type=TemplateVarType.INTEGER, default=113),
        TemplateVar(name="Player 2 Last Name Font Size", key="Player-2-Last-Name-Font-Size", type=TemplateVarType.INTEGER, default=113),
        TemplateVar(name="Player 3 Last Name Font Size", key="Player-3-Last-Name-Font-Size", type=TemplateVarType.INTEGER, default=113),
        TemplateVar(name="Player 4 Last Name Font Size", key="Player-4-Last-Name-Font-Size", type=TemplateVarType.INTEGER, default=113),
        TemplateVar(name="Player 5 Last Name Font Size", key="Player-5-Last-Name-Font-Size", type=TemplateVarType.INTEGER, default=113),
    ]),
    Template(name="Halftime Stats", template_file="/static/gfx/html/halftime-stats.html", vars=[
        TemplateVar(name="Home Stats (csv)", key="Home-Stats", type=TemplateVarType.STRING, default=""),
        TemplateVar(name="Away Stats (csv)", key="Away-Stats", type=TemplateVarType.STRING, default=""),
        TemplateVar(name="Home Score", key="Home-Score", type=TemplateVarType.STRING, default=""),
        TemplateVar(name="Away Score", key="Away-Score", type=TemplateVarType.STRING, default=""),
    ]),
    Template(name="Halftime Stats - Auto", template_file="/static/gfx/html/halftime-stats.html?livestats=true", vars=[]),
    Template(name="CAA Standings", template_file="/static/gfx/html/caa-standings.html", vars=[
        TemplateVar(name="Gender", key="gender", type=TemplateVarType.OPTION, choices=["mens", "womens"], default="mens")]
    ),
    Template(name="Starting Lineups", template_file="/static/gfx/html/starting-lineups.html", vars=[
        TemplateVar(name="Home Players", key="Home-Players", type=TemplateVarType.STRING, default=""),
        TemplateVar(name="Away Players", key="Away-Players", type=TemplateVarType.STRING, default=""),
    ]),
    Template(name="Wrestling Scorebug", template_file="/static/gfx/html/wrestling-scorebug.html", vars=[]),
    Template(name="Wrestling Probables", template_file="/static/gfx/html/wrestling-probables.html", vars=[]),
]