from typing import Optional
from structs import *
from inflection import underscore
from datetime import datetime
import json
from socketio import SimpleClient

MESSAGE_TYPE_MAPPING: dict[MessageType, BaseModel] = {
    MessageType.PING: Ping,
    MessageType.STATUS: Status,
    MessageType.TEAMS: Teams,
    MessageType.OFFICIALS: Officials,
    MessageType.BOXSCORE: Boxscore,
    # MessageType.ACTION: Action,
    # MessageType.PLAYBYPLAY: PlayByPlay
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

    _boxscore: Boxscore
    _live: SimpleClient = None

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

    def process_message(self, message: dict):
        message_type = message.get("type").upper()
        message = underscore_keys(message)
        with open(f"msg/{message_type}.json", "w") as f:
            f.write(json.dumps(message))
        if message_type in MESSAGE_TYPE_MAPPING:
            Struct = MESSAGE_TYPE_MAPPING[message_type]
            parsed = Struct(**message)
            if message_type == MessageType.BOXSCORE:
                self._boxscore = parsed
                self.emit("send_signal", dict(signal="newBoxscoreAvailable"))
            print("Got message of type", message_type)

    def command(self, command: dict):
        if command["type"] == "get_player_stats":
            self.get_player_stats(command["shirt"])

    def get_player_stats(self, shirt: str):
        pass