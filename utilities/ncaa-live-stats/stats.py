from structs import *
from inflection import underscore

MESSAGE_TYPE_MAPPING: dict[MessageType, msgspec.Struct] = {
    MessageType.PING: Ping,
    MessageType.STATUS: Status,
    MessageType.TEAMS: Teams,
    MessageType.OFFICIALS: Officials,
    MessageType.BOXSCORE: Boxscore,
    MessageType.ACTION: Action,
    MessageType.PLAYBYPLAY: PlayByPlay
}

class NCAALiveStats:

    _boxscore: Boxscore

    def process_message(self, message: dict):
        message_type = message.get("type")
        message = {underscore(k): v for k, v in message.items()}
        if message_type in MESSAGE_TYPE_MAPPING:
            Struct = MESSAGE_TYPE_MAPPING[message_type]
            parsed = Struct(message)
            if message_type == MessageType.BOXSCORE:
                self._boxscore = parsed
            print("Got message of type", message_type)

    def get_player_stats(self, shirt: str):
        pass