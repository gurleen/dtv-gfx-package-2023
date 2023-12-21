from typing import Literal
from strenum import StrEnum
from enum import auto
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


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
    REGULAR = auto()
    OVERTIME = auto()

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

class PlayerBox(BaseModel):
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

class TeamBox(BaseModel):
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
    lead_changes: int
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
    time_leading: float
    turnovers: int
    turnovers_team: int
    two_pointers_attempted: int
    two_pointers_made: int
    two_pointers_percentage: int

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
    GAME = auto()
    PERIOD = auto()
    TWO_PT = "2PT"
    THREE_PT = "3PT"
    FREETHROW = auto()
    JUMPBALL = auto()
    ASSIST = auto()
    BLOCK = auto()
    REBOUND = auto()
    FOUL = auto()
    FOULON = auto()
    TIMEOUT = auto()
    STEAL = auto()
    TURNOVER = auto()
    SUBSTITUTION = auto()
    HEADCOACHCHALLENGE = auto()

class ActionSubType:
    START = auto()
    END = auto()
    DUNK = auto()
    LAYUP = auto()
    FADEAWAY = auto()
    TIPIN = auto()
    JUMPSHOT = auto()
    ALLEYOOP = auto()
    DRIVINGLAYUP = auto()
    HOOKSHOT = auto()
    FLOATINGJUMPSHOT = auto()
    STEPBACKJUMPSHOT = auto()
    PULLUPJUMPSHOT = auto()
    TURNAROUNDJUMPSHOT = auto()
    WRONGBASKET = auto()
    ONEOFONE = "1of1"
    ONEOFTWO = "1of2"
    ONEOFTHREE = "1of3"
    TWOOFTWO = "2of2"
    TWOOFTHREE = "2of3"
    THREEOFTHREE = "3of3"
    STARTPERIOD = auto()
    UNCLEARPOSS = auto()
    LODGEDBALL = auto()
    HELDBALL = auto()
    BLOCKTIEUP = auto()
    OUTOFBOUNDS = auto()
    OUTOFBOUNDSREBOUND = auto()
    DOUBLEVIOLATION = auto()
    WON = auto()
    LOST = auto()
    OFFENSIVE = auto()
    PERSONAL = auto()
    TECHNICAL = auto()
    UNSPORTSMANLIKE = auto()
    DISQUALIFYING = auto()
    BENCHTECHNICAL = auto()
    COACHTECHNICAL = auto()
    ADMINTECHNICAL = auto()
    COACHDISQUALIFYING = auto()
    FULL = auto()
    SHORT = auto()
    OFFICIALS = auto()
    COMMERCIAL = auto()
    OFFENSIVEGOALTENDING = auto()
    LANEVIOLATION = auto()
    BALLHANDLING = auto()
    DRIBBLING = auto()
    BADPASS = auto()
    LOSTBALL = auto()
    OVERANDBACK = auto()
    BACKCOURT = auto()
    DOUBLEDRIBBLE = auto()
    TRAVEL = auto()
    SHOTCLOCK = auto()
    THREE_SEC = "3sec"
    FIVE_SEC = "5sec"
    EIGHT_SEC = "8sec"
    TEN_SEC = "10sec"
    TWENTY_FOUR_SEC = "24sec"
    OTHER = auto()
    IN = auto()
    OUT = auto()
    GAMEORSHOTCLOCK = auto()
    TWOPT = "2pt"
    THREEPT = "3pt"
    FREETHROW = auto()
    GOALORINTERFERENCE = auto()
    FOUL = auto()
    VIOLENCE = auto()

class Action(BaseModel):
    message_id: int
    action_number: int
    team_number: int
    pno: int
    clock: str
    shot_clock: str
    time_actual: datetime
    period: int
    period_type: PeriodType
    action_type: ActionType
    success: bool
    sub_type: ActionSubType
    qualifiers: list[str]
    value: str
    previous_action: int
    official_id: int
    x: float
    y: float
    area: str
    side: Literal["", "left", "right"]
    score1: str
    score2: str
    edited: datetime
    inserted: datetime
    deleted: datetime
    orig_message_id: int

class PlayByPlay(BaseModel):
    actions: list[Action]


