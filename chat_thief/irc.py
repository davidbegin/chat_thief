from typing import List, Dict
import json
import os
import socket


from chat_thief.log import logger
from chat_thief.config.twitch import TwitchConfig

ENCODING = "utf-8"
CHAT_MSG = "PRIVMSG"
CONNECTION_DATA = ("irc.chat.twitch.tv", 6667)

config = TwitchConfig()


def _irc_handshake(server: socket.socket) -> None:
    logger.debug(
        json.dumps({"message": f"Connecting to #{config.channel} as {config.bot}"})
    )
    server.sendall(bytes("PASS " + config.token + "\r\n", ENCODING))
    server.sendall(bytes("NICK " + config.bot + "\r\n", ENCODING))
    server.sendall(bytes("JOIN " + f"#{config.channel}" + "\r\n", ENCODING))


def send_twitch_msg(msg):
    with socket.socket() as server:
        server.connect(CONNECTION_DATA)
        _irc_handshake(server)
        if msg:
            if "BLOCK_TWITCH_MSGS" in os.environ:
                print(msg)
            else:
                server.sendall(
                    bytes(f"{CHAT_MSG} #{config.channel} :{msg}\n", ENCODING)
                )
