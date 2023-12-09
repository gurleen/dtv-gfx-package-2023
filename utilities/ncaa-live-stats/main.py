import configparser
import socket
from threading import Thread
import socketio

import msgspec
from boltons.socketutils import BufferedSocket

from stats import NCAALiveStats
from structs import ConnectionParams


CONFIG_FILE_NAME = "livestats.config"
READ_LIMIT = 2097152
LINE_DELIM = b"\r\n"

class Config(msgspec.Struct):
    hostname: str
    port: int


def read_config() -> Config:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)
    return Config(**dict(config["DEFAULT"]))

def create_socket(config: Config) -> BufferedSocket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ("10.248.65.90", 7677)
    sock.bind(host)
    return BufferedSocket(sock, maxsize=READ_LIMIT, timeout=None)

def write_struct_to_sock(sock: BufferedSocket, struct: msgspec.Struct):
    formatted = msgspec.json.encode(struct)
    sock.send(formatted)

def read_from_socket(sock: BufferedSocket, nls: NCAALiveStats):
    decoder = msgspec.json.Decoder()
    while True:
        message = sock.recv_until(LINE_DELIM)
        decoded = decoder.decode(message)
        nls.process_message(decoded)

def listen_thread(sock: BufferedSocket, nls: NCAALiveStats):
    
    read_from_socket(sock, nls)

def main():
    config = read_config()
    sock = create_socket(config)
    params = ConnectionParams()
    write_struct_to_sock(sock, params)
    nls = NCAALiveStats()
    listener = Thread(target=listen_thread, args=(sock, nls))
    listener.start()
    with socketio.SimpleClient() as sio:
        sio.connect("https://livestats.gurleen.dev")
        while True:
            msg = sio.receive()
            if msg[0] == "update":
                payload = msg[1]
                if payload["key"] == "homePlayerStat":
                    pass




if __name__ == "__main__":
    main()