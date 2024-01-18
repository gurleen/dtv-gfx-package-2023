from pydantic import BaseModel, Field, AliasPath
from typing import Optional


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
    group_id: int
    conference_short_name: str
    conference_name: str
    conference_id: int
    logo_name: str
    website: str
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


class Boxscore(BaseModel):
    fg: Optional[str] = None
    fg_pct: Optional[str] = Field(None, alias="field goal %")
    three_pt: Optional[str] = Field(None, alias="3pt")
    three_pt_pct: Optional[str] = Field(None, alias="three point %")
    ft: Optional[str] = None
    ft_pct: Optional[str] = Field(None, alias="free throw %")
    reb: Optional[str] = Field(None, alias="rebounds")
    off_reb: Optional[str] = Field(None, alias="offensive rebounds")
    def_reb: Optional[str] = Field(None, alias="defensive rebounds")
    ast: Optional[str] = Field(None, alias="assists")
    stl: Optional[str] = Field(None, alias="steals")
    blk: Optional[str] = Field(None, alias="blocks")
    to: Optional[str] = Field(None, alias="turnovers")
    pip: Optional[str] = Field(None, alias="points in paint")
    fouls: Optional[str] = Field(None, alias="fouls")
    ll: Optional[str] = Field(None, alias="largest lead")


class FullBox(BaseModel):
    home: Boxscore
    away: Boxscore
