from typing import List, Dict
import json
import socket

from chat_thief.log import logger
from chat_thief.config import TwitchConfig
from chat_thief.command_parser import CommandParser

CONNECTION_DATA = ("irc.chat.twitch.tv", 6667)
ENCODING = "utf-8"
CHAT_MSG = "PRIVMSG"
ARE_YOU_ALIVE = "PING"
I_AM_ALIVE = "PONG"

config = TwitchConfig()


def pong(server: socket.socket) -> None:
    server.sendall(bytes(I_AM_ALIVE + "\r\n", ENCODING))


def send_msg(server: socket.socket, msg: str) -> None:
    if msg:
        server.sendall(bytes(f"{CHAT_MSG} #{config.channel} :{msg}\n", ENCODING))


def irc_handshake(server: socket.socket) -> None:
    logger.info(
        json.dumps({"message": f"Connecting to #{config.channel} as {config.bot}"})
    )

    server.sendall(bytes("PASS " + config.token + "\r\n", ENCODING))
    server.sendall(bytes("NICK " + config.bot + "\r\n", ENCODING))
    server.sendall(bytes("JOIN " + f"#{config.channel}" + "\r\n", ENCODING))


def run_bot(server: socket.socket) -> None:
    while True:
        irc_response = server.recv(2048).decode(ENCODING).split()

        if irc_response[0] == ARE_YOU_ALIVE:
            pong(server)
        elif len(irc_response) < 2:
            pass
        elif irc_response[1] == CHAT_MSG:
            if response := CommandParser(irc_response, logger).build_response():
                send_msg(server, response)


if __name__ == "__main__":
    with socket.socket() as server:
        server.connect(CONNECTION_DATA)
        irc_handshake(server)
        run_bot(server)
