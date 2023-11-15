from .structs import *

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

    def process_message(message: dict):
        message_type = message.get("type")
        if message_type in MESSAGE_TYPE_MAPPING:
            Struct = MESSAGE_TYPE_MAPPING[message_type]
            parsed = Struct(message)
            print("Got message of type", message_type)