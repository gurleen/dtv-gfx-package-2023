from typing import Any, Literal, Optional
from enum import auto, Enum
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel
from pydantic import computed_field
from strenum.mixins import Comparable
from strenum import StrEnum


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class ComputedStatMixin:
    @computed_field
    @property
    def field_goals(self) -> str:
        return f"{self.field_goals_made}-{self.field_goals_attempted}"

    @computed_field
    @property
    def three_pointers(self) -> str:
        return f"{self.three_pointers_made}-{self.three_pointers_attempted}"
    
    @computed_field
    @property
    def free_throws(self) -> str:
        return f"{self.free_throws_made}-{self.free_throws_attempted}"


class MessageType(StrEnum):
    PING = auto()
    STATUS = auto()
    SETUP = auto()
    TEAMS = auto()
    OFFICIALS = auto()
    BOXSCORE = auto()
    ACTION = auto()
    PLAYBYPLAY = auto()

class ConnectionParams(BaseModel):
    type: str = "parameters"
    types: str = "se,ac,mi,te,box,pbp"
    playbyplayOnConnect: int = 0
    fromMessageId: int = 0


class Ping(BaseModel):
    timestamp: str


class MatchStatus(StrEnum):
    READY = auto()
    WARMUP = auto()
    PREMATCH = auto()
    ANTHEM = auto()
    ONCOURT = auto()
    COUNTDOWN = auto()
    INPROGRESS = auto()
    PERIODBREAK = auto()
    INTERRUPTED = auto()
    CANCELLED = auto()
    FINISHED = auto()
    PROTESTED = auto()
    COMPLETE = auto()
    RESCHEDULED = auto()
    DELAYED = auto()

class PeriodType(StrEnum):
    REGULAR = "REGULAR"
    OVERTIME = "OVERTIME"

class PeriodStatus(StrEnum):
    PENDING = auto()
    STARTED = auto()
    ENDED = auto()
    CONFIRMED = auto()

class Period(BaseModel):
    current: int
    period_type: PeriodType

class Score(BaseModel):
    team_number: int
    score: int
    timeouts_remaining: int
    fouls: int
    team_fouls: int

class Status(BaseModel):
    status: MatchStatus
    period: Period
    clock: str
    shot_clock: str
    clock_running: bool
    possession: int
    possessionArrow: int
    scores: list[Score]

class TeamRecordDetail(BaseModel):
    team_name: str
    team_id: int
    team_code: str
    team_code_long: str
    is_home_competitor: bool

class Player(BaseModel):
    pno: int
    person_id: int
    family_name: str
    first_name: str
    height: float
    shirt_number: str
    playing_position: str
    starter: bool
    active: bool

class TeamRecord(BaseModel):
    team_number: int
    detail: TeamRecordDetail
    players: list[Player]


class Teams(BaseModel):
    teams: list[TeamRecord]


class Referee:
    family_name: str
    first_name: str

class Officials(BaseModel):
    referee1: Referee
    referee2: Referee
    referee3: Referee

# --- BOXSCORE ---

class PlayerBox(BaseModel, ComputedStatMixin):
    pno: int
    assists: int
    blocks: int
    blocks_received: int
    efficiency: int
    fast_break_points_made: int
    field_goals_attempted: int
    field_goals_made: int
    field_goals_percentage: float
    fouls_on: int
    fouls_personal: int
    fouls_technical: int
    free_throws_attempted: int
    free_throws_made: int
    free_throws_percentage: float
    minutes: float
    plus_minus_points: int
    points: int
    points_fast_break: int
    points_from_turnovers: int
    points_in_the_paint: int
    points_in_the_paint_made: int
    points_second_chance: int
    rebounds_defensive: int
    rebounds_offensive: int
    rebounds_total: int
    second_chance_points_made: int
    steals: int
    three_pointers_attempted: int
    three_pointers_made: int
    three_pointers_percentage: float
    turnovers: int
    two_pointers_attempted: int
    two_pointers_made: int
    two_pointers_percentage: float

class TeamBox(BaseModel, ComputedStatMixin):
    assists: int
    bench_points: int
    biggest_lead: int
    biggest_scoring_run: int
    blocks: int
    blocks_received: int
    efficiency: float
    fast_break_points_made: int
    points_from_turnovers: int
    field_goals_attempted: int
    field_goals_made: int
    field_goals_percentage: float
    fouls_on: int
    fouls_personal: int
    fouls_team: int
    fouls_technical: int
    free_throws_attempted: int
    free_throws_made: int
    free_throws_percentage: float
    minutes: float
    points: int
    points_fast_break: int
    points_in_the_paint: int
    points_in_the_paint_made: int
    points_second_chance: int
    rebounds_defensive: int
    rebounds_offensive: int
    rebounds_personal: int
    rebounds_team: int
    rebounds_team_defensive: int
    rebounds_team_offensive: int
    rebounds_total: int
    rebounds_total_defensive: int
    rebounds_total_offensive: int
    second_chance_points_made: int
    steals: int
    three_pointers_attempted: int
    three_pointers_made: int
    three_pointers_percentage: float
    turnovers: int
    turnovers_team: int
    two_pointers_attempted: int
    two_pointers_made: int
    two_pointers_percentage: float

class BoxscoreTotal(BaseModel):
    players: list[PlayerBox]
    team: TeamBox

class BoxscorePeriod(BaseModel):
    period: int
    period_type: PeriodType
    players: list[PlayerBox]
    team: TeamBox

class BoxscoreTeam(BaseModel):
    team_number: int
    total: BoxscoreTotal
    periods: list[BoxscorePeriod]

class Boxscore(BaseModel):
    teams: list[BoxscoreTeam]
    # total: BoxscoreTotal
    # periods: list[BoxscorePeriod]

# --- ACTION ---
class ActionType(StrEnum):
    game = auto()
    period = auto()
    two_pt = "2pt"
    three_pt = "3pt"
    freethrow = auto()
    jumpball = auto()
    assist = auto()
    block = auto()
    rebound = auto()
    foul = auto()
    foulon = auto()
    timeout = auto()
    steal = auto()
    turnover = auto()
    substitution = auto()
    headcoachchallenge = auto()
    other = auto()

    @classmethod
    def _missing_(cls, value: object) -> Any:
        return cls.other
    
SCORING_ACTION_TYPES = [ActionType.two_pt, ActionType.three_pt, ActionType.freethrow]

class ActionSubType(StrEnum):
    start = auto()
    end = auto()
    dunk = auto()
    layup = auto()
    fadeaway = auto()
    tipin = auto()
    jumpshot = auto()
    alleyoop = auto()
    drivinglayup = auto()
    hookshot = auto()
    floatingjumpshot = auto()
    stepbackjumpshot = auto()
    pullupjumpshot = auto()
    turnaroundjumpshot = auto()
    wrongbasket = auto()
    oneofone = "1of1"
    oneoftwo = "1of2"
    oneofthree = "1of3"
    twooftwo = "2of2"
    twoofthree = "2of3"
    threeofthree = "3of3"
    startperiod = auto()
    unclearposs = auto()
    lodgedball = auto()
    heldball = auto()
    blocktieup = auto()
    outofbounds = auto()
    outofboundsrebound = auto()
    doubleviolation = auto()
    won = auto()
    lost = auto()
    offensive = auto()
    personal = auto()
    technical = auto()
    unsportsmanlike = auto()
    disqualifying = auto()
    benchtechnical = auto()
    coachtechnical = auto()
    admintechnical = auto()
    coachdisqualifying = auto()
    full = auto()
    short = auto()
    officials = auto()
    commercial = auto()
    offensivegoaltending = auto()
    laneviolation = auto()
    ballhandling = auto()
    dribbling = auto()
    badpass = auto()
    lostball = auto()
    overandback = auto()
    backcourt = auto()
    doubledribble = auto()
    travel = auto()
    shotclock = auto()
    three_sec = "3sec"
    five_sec = "5sec"
    eight_sec = "8sec"
    ten_sec = "10sec"
    twenty_four_sec = "24sec"
    other = auto()
    _in = "in"
    out = auto()
    gameorshotclock = auto()
    twopt = "2pt"
    threept = "3pt"
    freethrow = auto()
    goalorinterference = auto()
    foul = auto()
    violence = auto()

    @classmethod
    def _missing_(cls, value: object) -> Any:
        return cls.other


class Action(BaseModel):
    action_number: int
    team_number: Optional[int] = None
    pno: Optional[int] = None
    clock: str
    shot_clock: Optional[str] = None
    time_actual: Optional[datetime] = None
    period: Optional[int] = None
    period_type: Optional[PeriodType] = None
    action_type: ActionType
    success: Optional[bool] = None
    sub_type: Optional[ActionSubType] = None
    qualifiers: list[str] = None
    value: Optional[str] = None
    previous_action: Optional[int] = None
    official_id: Optional[int] = None
    x: Optional[float] = None
    y: Optional[float] = None
    area: Optional[str] = None
    side: Literal["", "left", "right"] #
    score1: int #
    score2: int #
    edited: Optional[datetime] = None
    inserted: Optional[datetime] = None
    deleted: Optional[datetime] = None
    orig_message_id: Optional[int] = None

class PlayByPlay(BaseModel):
    actions: list[Action]


