from typing import Optional
from structs import *
from inflection import underscore
from first import first
import json
from socketio import SimpleClient

DEBUG = False

MESSAGE_TYPE_MAPPING: dict[MessageType, BaseModel] = {
    MessageType.PING.value: Ping,
    MessageType.STATUS.value: Status,
    MessageType.TEAMS.value: Teams,
    MessageType.OFFICIALS.value: Officials,
    MessageType.BOXSCORE.value: Boxscore,
    MessageType.ACTION.value: Action,
    MessageType.PLAYBYPLAY.value: PlayByPlay
}

STAT_ABBR_MAP = {
    "rebounds_total": "REB",
    "assists": "AST",
    "steals": "STL",
    "blocks": "BLK",
    "turnovers": "TO"
}

def format_key(key: str):
    key = underscore(key)
    if key.startswith("s_"):
        key = key[2:]
    return key

def underscore_keys(obj):
    if isinstance(obj, dict):
        return {format_key(k): underscore_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [underscore_keys(i) for i in obj]
    else:
        return obj

class NCAALiveStats:

    _boxscore: Boxscore = None
    _live: SimpleClient = None
    _home_id: int = -1
    _away_id: int = -1
    _shirt_map: dict[str, dict[str, str]]   # side -> { shirt -> pno }
    _pno_map: dict[str, dict[str, str]]   # side -> { pno -> shirt }
    _pbp: list[Action]


    def __init__(self):
        self._shirt_map = dict(home={}, away={})
        self._pno_map = dict(home={}, away={})
        self._pbp = []

    def is_home(self, team_number: str) -> bool:
        return team_number == self._home_id
    
    def add_live_connection(self, live: SimpleClient):
        print("Adding live connection")
        self._live = live

    def emit(self, event: str, data: Optional[dict] = None):
        if self._live is None:
            return
        print("Emitting:", event, data)
        if data is None:
            self._live.emit(event)
        else:
            self._live.emit(event, data)

    def handle_boxscore(self, message: Boxscore):
        self._boxscore = message
        self.emit("send_signal", dict(signal="newBoxscoreAvailable"))

    def handle_teams(self, message: Teams):
        for team in message.teams:
            if team.detail.is_home_competitor:
                self._home_id = team.team_number
            else:
                self._away_id = team.team_number

            side = "home" if team.detail.is_home_competitor else "away"
            for player in team.players:
                self._shirt_map[side][player.shirt_number] = player.pno
                self._pno_map[side][player.pno] = player.shirt_number

    def handle_playbyplay(self, message: PlayByPlay):
        print(f"Got play by play, {len(message.actions)} actions")
        self._pbp.extend(message.actions)
        self.calculate_scoring_drought("home")
        self.calculate_scoring_drought("away")

    def handle_action(self, message: Action):
        self._pbp.append(message)
        self.calculate_scoring_drought("home")
        self.calculate_scoring_drought("away")

    def process_message(self, message: dict):
        message_type = message.get("type").upper()
        message = underscore_keys(message)
        if DEBUG:
            print(message_type)
        with open(f"msg/{message_type}.json", "w") as f:
            f.write(json.dumps(message))
        if message_type in MESSAGE_TYPE_MAPPING:
            Struct = MESSAGE_TYPE_MAPPING[message_type]
            parsed = Struct(**message)
            mtype = MessageType(message_type)
            if mtype == MessageType.BOXSCORE:
                self.handle_boxscore(parsed)
            elif mtype == MessageType.TEAMS:
                self.handle_teams(parsed)
            elif mtype == MessageType.PLAYBYPLAY:
                self.handle_playbyplay(parsed)
            elif mtype == MessageType.ACTION:
                self.handle_action(parsed)

    def command(self, command: dict):
        if command["type"] == "get_player_stats":
            self.get_player_stats(command["shirt"])

    def get_home_stats(self) -> BoxscoreTotal:
        return first(self._boxscore.teams, key=lambda t: t.team_number == self._home_id).total
    
    def get_away_stats(self) -> BoxscoreTotal:
        return first(self._boxscore.teams, key=lambda t: t.team_number == self._away_id).total

    def get_boxscore(self):
        home_stats: BoxscoreTotal = self.get_home_stats()
        away_stats: BoxscoreTotal = self.get_away_stats()
        return dict(
            home=dict(
                team=home_stats.team.model_dump(),
                players={self._pno_map["home"][pbox.pno]: pbox.model_dump() for pbox in home_stats.players}
            ),
            away=dict(
                team=away_stats.team.model_dump(),
                players={self._pno_map["away"][pbox.pno]: pbox.model_dump() for pbox in away_stats.players}
            )
        )
    
    def get_stats_for_halftime(self):
        home_stats = self.get_home_stats().team
        away_stats = self.get_away_stats().team
        stats = ["field_goals", "three_pointers", "free_throws", "rebounds_total", "turnovers"]

        return dict(
            home=[getattr(home_stats, k) for k in stats],
            away=[getattr(away_stats, k) for k in stats]
        )
    
    def get_play_by_play(self):
        return [action.model_dump() for action in self._pbp]
    
    def get_player_stats(self, side: str, shirt: str):
        pno = self._shirt_map[side][shirt]
        stats = first(self.get_home_stats().players, key=lambda p: p.pno == pno)
        return stats.model_dump()
    
    def calculate_scoring_drought(self, side: Literal["home", "away"]):
        team_id = self._home_id if side == "home" else self._away_id
        for action in reversed(self._pbp):
            if action.team_number == team_id and action.action_type in SCORING_ACTION_TYPES and action.success:
                print(side, "last score", action.clock)

    def get_player_stat_line(self, side: str, shirt: str):
        pno = self._shirt_map[side][shirt]
        stats = first(self.get_home_stats().players, key=lambda p: p.pno == pno)
        stat_names = ["rebounds_total", "assists", "steals", "blocks", "turnovers"]
        stat_line = []
        if stats.points > 0:
            stat_line.append(f"{stats.points} PTS")
        
        top_n = 3 if not stat_line else 2
        stat_names.sort(key=lambda s: getattr(stats, s), reverse=True)
        for i in range(top_n):
            value = getattr(stats, stat_names[i])
            if value > 0:
                stat_line.append(f"{value} {STAT_ABBR_MAP[stat_names[i]]}")

        return " | ".join(stat_line)