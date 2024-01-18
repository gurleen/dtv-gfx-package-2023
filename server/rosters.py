import csv
from pathlib import Path
from typing import Literal
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import requests
from perscache import Cache
from loguru import logger
from team_models import Player, Team, Boxscore, FullBox
from images import ensure_team_dirs
from app import DATA_PATH


router = APIRouter()
cache = Cache()
ROSTER_API_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/{gender}-college-basketball/teams/{team_id}/roster"
TEAM_API_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/{gender}-college-basketball/teams/{team_id}"
EVENT_API_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/{gender}-college-basketball/summary?event={event_id}"
NCAA_BOXSCORE_URL = "https://data.ncaa.com/casablanca/game/{game_id}/boxscore.json"
CAA_STANDINGS_URL = "https://site.web.api.espn.com/apis/v2/sports/basketball/{gender}-college-basketball/standings?group=10"
ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/{gender}-college-basketball/scoreboard?groups=10"


with open("espn_mbb_teams.csv", "r") as f:
    reader = csv.DictReader(f)
    TEAMS = {int(row["team_id"]) : Team(**row) for row in reader}


@router.get("/teams")
async def get_teams() -> dict[int, Team]:
    return TEAMS

@router.get("/teams/short") 
async def get_teams_short() -> list[dict]:
    return [dict(id=team.team_id, name=team.display_name) for team in TEAMS.values()]

@cache
def get_roster_for_team(gender: str, team_id: int) -> list[Player]:
    logger.info(f"Cache miss for {gender} team {team_id}, getting from ESPN...")
    players = []
    api_url = ROSTER_API_URL.format(gender=gender, team_id=team_id)
    response = requests.get(api_url).json()
    for item in response["athletes"]:
        parsed_athlete = Player(**item)
        players.append(parsed_athlete)
    logger.info(f"Got roster info for {len(players)} players on team {team_id}")
    return players

@router.get("/teams/{gender}/{team_id}")
def get_team(gender: str, team_id: int) -> Team:
    team = TEAMS[team_id]
    team.players = get_roster_for_team(gender, team_id)
    return team

@router.get("/teams/{gender}/{team_id}/players")
def get_players_for_team(gender: str, team_id: int) -> list[Player]:
    return get_roster_for_team(gender, team_id)

@router.get("/teams/{gender}/{team_id}/players/{jersey}")
def get_player(gender: str, team_id: int, jersey: str) -> Player:
    roster = get_roster_for_team(gender, team_id)
    player = next((x for x in roster if x.jersey == jersey), None)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

def get_team_by_id(id: int) -> Team:
    id = int(id)
    return TEAMS[id]

def get_team_json(gender: str, id: int) -> dict:
    url = TEAM_API_URL.format(gender=gender, team_id=id)
    return requests.get(url).json()

def get_live_game_id(gender: str, id: int) -> str:
    team = get_team_json(gender, id)
    return team["team"]["nextEvent"][0]["id"]

def parse_team_stats(stats: list[dict]) -> Boxscore:
    stats_pivot = {s["label"].lower() : s["displayValue"] for s in stats}
    print(stats_pivot)
    return Boxscore(**stats_pivot)


def get_mens_live_stats(game_id: str, home_id: int = None) -> FullBox:
    url = EVENT_API_URL.format(gender="mens", event_id=game_id)
    response = requests.get(url).json()
    teams = response["boxscore"]["teams"]
    if home_id is None:
        home_team = teams[0]
        away_team = teams[1]
    else:
        home_team = next((x for x in teams if x["team"]["id"] == str(home_id)))
        away_team = next((x for x in teams if x["team"]["id"] != str(home_id)))
    home_stats = parse_team_stats(home_team["statistics"])
    away_stats = parse_team_stats(away_team["statistics"])
    return FullBox(home=home_stats, away=away_stats)
    

def get_womens_live_stats(game_id: str) -> FullBox:
    url = NCAA_BOXSCORE_URL.format(game_id=game_id)
    response = requests.get(url).json()
    first_home = response["meta"]["teams"][0]["homeTeam"]
    first_box_raw = response["teams"][0]["playerTotals"]
    first_box = Boxscore(
        fg=first_box_raw["fieldGoalsMade"],
        three_fg=first_box_raw["threePointsMade"],
        ft=first_box_raw["freeThrowsMade"],
        reb=first_box_raw["totalRebounds"],
        off_reb=first_box_raw["offensiveRebounds"],
        ast=first_box_raw["assists"],
        stl=first_box_raw["steals"],
        to=first_box_raw["turnovers"],
        blk=first_box_raw["blockedShots"],
        fg_pct=first_box_raw["fieldGoalPercentage"].replace("-", "0%"),
        three_pt_pct=first_box_raw["threePointPercentage"].replace("-", "0%"),
        ft_pct=first_box_raw["freeThrowPercentage"].replace("-", "0%"),
    )
    second_box_raw = response["teams"][1]["playerTotals"]
    second_box = Boxscore(
        fg=second_box_raw["fieldGoalsMade"],
        three_fg=second_box_raw["threePointsMade"],
        ft=second_box_raw["freeThrowsMade"],
        reb=second_box_raw["totalRebounds"],
        off_reb=second_box_raw["offensiveRebounds"],
        ast=second_box_raw["assists"],
        stl=second_box_raw["steals"],
        to=second_box_raw["turnovers"],
        blk=second_box_raw["blockedShots"],
        fg_pct=second_box_raw["fieldGoalPercentage"].replace("-", "0%"),
        three_pt_pct=second_box_raw["threePointPercentage"].replace("-", "0%"),
        ft_pct=second_box_raw["freeThrowPercentage"].replace("-", "0%"),
    )
    return FullBox(home=first_box, away=second_box) if first_home else FullBox(home=second_box, away=first_box)


@router.get("/live/{gender}/{game_id}")
def get_live_stats(gender: str, game_id, home_id: int = None) -> FullBox:
    if gender == "mens":
        return get_mens_live_stats(game_id, home_id)
    elif gender == "womens":
        return get_womens_live_stats(game_id)
    

@router.get("/standings/{gender}")
def get_caa_standings(gender: str):
    url = CAA_STANDINGS_URL.format(gender=gender)
    response = requests.get(url).json()
    teams = []
    for team in response["standings"]["entries"]:
        team_id = int(team["team"]["id"])
        item = dict(
            team=TEAMS[team_id],
            overall=next(x for x in team["stats"] if x["name"] == "overall")["displayValue"],
            overall_pct=next(x for x in team["stats"] if x["name"] == "winPercent")["value"],
            conf=next(x for x in team["stats"] if x["name"] == "vs. Conf.")["displayValue"],
            conf_pct=next(x for x in team["stats"] if x["name"] == "leagueWinPercent")["value"],
        )
        teams.append(item)
    return sorted(teams, key=lambda x: (x["conf_pct"], x["overall_pct"]), reverse=True)


@router.get("/scoreboard/{gender}")
def get_scoreboard(gender: str):
    url = ESPN_SCOREBOARD_URL.format(gender=gender)
    response = requests.get(url).json()
    games = []
    for game in response["events"]:
        status = game["status"]["type"]["shortDetail"]
        if " - " in status:
            status = status.split(" - ")[1]
        this_game = dict(
            id=game["id"],
            away=get_team_by_id(game["competitions"][0]["competitors"][0]["team"]["id"]),
            home=get_team_by_id(game["competitions"][0]["competitors"][1]["team"]["id"]),
            awayScore=game["competitions"][0]["competitors"][0]["score"],
            homeScore=game["competitions"][0]["competitors"][1]["score"],
            status=status
        )
        games.append(this_game)
    return games


@router.get("/headshot/{team_id}/{gender}/{shirt}")
def get_roster_image(team_id: int, gender: Literal["mens", "womens"], shirt: str):
    team = get_team_by_id(team_id)
    dir = ensure_team_dirs(team, gender)
    filename = f"{shirt}.png"
    return FileResponse(Path(dir, filename), media_type="image/png")


@router.get("/video/{fname}")
def get_media(fname: str):
    path = Path(DATA_PATH, "media", fname)
    print(path)
    return FileResponse(path)