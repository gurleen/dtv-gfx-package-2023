import configparser
import socket
from threading import Thread
from typing import Optional
import socketio
from queue import Queue

import json
from pydantic import BaseModel
from boltons.socketutils import BufferedSocket

from stats import NCAALiveStats
from structs import ConnectionParams


CONFIG_FILE_NAME = "livestats.config"
READ_LIMIT = 2097152
LINE_DELIM = b"\r\n"

class Config(BaseModel):
    hostname: str
    port: int


def read_config() -> Config:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)
    return Config(**dict(config["DEFAULT"]))

def create_socket(config: Config) -> BufferedSocket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = (config.hostname, config.port)
    print(host)
    sock.connect(host)
    return BufferedSocket(sock, maxsize=READ_LIMIT, timeout=None)

def write_struct_to_sock(sock: BufferedSocket, struct: BaseModel):
    formatted = BaseModel.model_dump(struct)
    dumped = json.dumps(formatted)
    print(dumped)
    encoded = dumped.encode("utf-8")
    sock.send(encoded + LINE_DELIM)

def has_command(queue: Queue) -> Optional[dict]:
    try:
        return queue.get_nowait()
    except:
        return None

def read_from_socket(sock: BufferedSocket, nls: NCAALiveStats):
    message = sock.recv_until(LINE_DELIM, maxsize=READ_LIMIT, timeout=None)
    decoded = json.loads(message)
    nls.process_message(decoded)

def listen_thread(sock: BufferedSocket, nls: NCAALiveStats, queue: Queue):
    while True:
        if command := has_command(queue):
            print(command)
            nls.command(command)
        read_from_socket(sock, nls)


def main():
    config = read_config()
    msg_queue = Queue()
    sock = create_socket(config)
    params = ConnectionParams()
    write_struct_to_sock(sock, params)
    nls = NCAALiveStats()
    listener = Thread(target=listen_thread, args=(sock, nls, msg_queue))
    listener.start()
    with socketio.SimpleClient() as sio:
        sio.connect("https://livestats.gurleen.dev")
        nls.add_live_connection(sio)
        while True:
            msg = sio.receive()
            if msg[0] == "liveStatsCommand":
                msg_queue.put(msg[1])




if __name__ == "__main__":
    main()