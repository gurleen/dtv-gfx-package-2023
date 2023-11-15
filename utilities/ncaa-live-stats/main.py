import configparser
import socket
import json

import msgspec
from boltons.socketutils import BufferedSocket

from .stats import NCAALiveStats
from .structs import ConnectionParams


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
    sock.bind((config.hostname, config.port))
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

def main():
    config = read_config()
    sock = create_socket(config)
    params = ConnectionParams()
    write_struct_to_sock(sock, params)
    nls = NCAALiveStats()
    read_from_socket(sock, nls)



if __name__ == "__main__":
    main()