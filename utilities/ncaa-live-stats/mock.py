from flask import Flask
import json
from stats import NCAALiveStats
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
nls = NCAALiveStats()

for file in ["SETUP", "TEAMS", "PLAYBYPLAY", "BOXSCORE"]:
    with open(f"msg/{file}.json", "r") as f:
        message = json.loads(f.read())
        nls.process_message(message)

@app.route("/box")
def boxscore():
    return nls.get_boxscore()

@app.route("/half")
def half():
    return nls.get_stats_for_halftime()

@app.route("/pbp")
def pbp():
    return nls.get_play_by_play()

@app.route("/player/<side>/<player_id>")
def player(side, player_id):
    return nls.get_player_stats(side, player_id)

@app.route("/player/<side>/<player_id>/line")
def team_line(side, player_id):
    return {"line": nls.get_player_stat_line(side, player_id)}


if __name__ == "__main__":
    app.run(port=8081)