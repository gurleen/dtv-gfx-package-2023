import csv
from typing import Literal, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, AliasPath
import requests
from perscache import Cache
from loguru import logger


router = APIRouter()
cache = Cache()
# ROSTER_API_URL = "https://sports.core.api.espn.com/v2/sports/basketball/leagues/{gender}-college-basketball/seasons/2024/teams/{team_id}/athletes?lang=en%C2%AEion=us"
ROSTER_API_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/{gender}-college-basketball/teams/{team_id}/roster"


class Team(BaseModel):
    team_id: int
    abbreviation: str
    display_name: str
    short_name: str
    mascot: str
    nickname: str
    team: str
    color: str
    alternate_color: str
    logo: str
    logo_dark: str
    href: str
    conference_url: str
    group_id: int
    conference_short_name: str
    conference_uid: str
    conference_name: str
    conference_logo: str
    parent_group_id: int
    conference_id: int
    logo_name: str
    players: Optional[list["Player"]] = None

    @property
    def white_logo(self) -> str:
        return f"/media/logos-white/{self.logo_name}"

class Player(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    display_height: str = Field(alias="displayHeight")
    birth_city: str = Field(alias=AliasPath("birthPlace", "city"))
    birth_country: str = Field(alias=AliasPath("birthPlace", "country"))
    jersey: str
    slug: str
    position: str = Field(alias=AliasPath("position", "abbreviation"))
    year_full: str = Field(alias=AliasPath("experience", "displayValue"))
    year: str = Field(alias=AliasPath("experience", "abbreviation"))


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
def get_team(gender: Literal["womens", "mens"], team_id: int) -> Team:
    team = TEAMS[team_id]
    team.players = get_roster_for_team(gender, team_id)
    return team

@router.get("/teams/{gender}/{team_id}/players")
def get_players_for_team(gender: Literal["womens", "mens"], team_id: int) -> list[Player]:
    return get_roster_for_team(gender, team_id)

@router.get("/teams/{gender}/{team_id}/players/{jersey}")
def get_player(gender: Literal["womens", "mens"], team_id: int, jersey: str) -> Player:
    player = next((x for x in get_roster_for_team(gender, team_id) if x.jersey == jersey), None)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

def get_team_by_id(id: int) -> Team:
    id = int(id)
    return TEAMS[id]