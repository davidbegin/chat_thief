import json
import logging
import os
import socket
import sys
import time
from pathlib import Path

from log import Log
from config import TwitchConfig
from command_parser import CommandParser

CONNECTION_DATA = ("irc.chat.twitch.tv", 6667)
ENCODING      = "utf-8"
CHAT_MSG      = "PRIVMSG"
ARE_YOU_ALIVE = "PING"
I_AM_ALIVE    = "PONG"

config = TwitchConfig(channel="zabt2")
logger = Log()


def pong(server):
    server.sendall(bytes(I_AM_ALIVE + "\r\n", ENCODING))


def send_msg(server, msg):
    if msg:
        result = server.sendall(
            bytes(f"{CHAT_MSG} #{config.channel} :{msg}\n", ENCODING)
        )


def irc_handshake(server):
    logger.debug(json.dumps({"message": f"Connecting to #{config.channel} as {config.bot}"}))

    server.sendall(bytes("PASS " + config.token + "\r\n", ENCODING))
    server.sendall(bytes("NICK " + config.bot + "\r\n", ENCODING))
    server.sendall(bytes("JOIN " + f"#{config.channel}" + "\r\n", ENCODING))


def run_bot(server):
    while True:
        irc_response = server.recv(2048).decode(ENCODING).split()

        if irc_response[1] == CHAT_MSG:
            if response:= CommandParser(irc_response, logger).build_response():
                send_msg(server,  response)
        elif irc_response[0] == ARE_YOU_ALIVE:
            pong(server)


if __name__ == "__main__":
    # Should we add explicit params of: AF_INET and SOCK_STREAM
    with socket.socket() as server:
        server.connect(CONNECTION_DATA)
        irc_handshake(server)
        run_bot(server)
