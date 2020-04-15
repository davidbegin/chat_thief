from typing import List, Dict
import json
import socket
import asyncio
import traceback

from chat_thief.log import logger
from chat_thief.config import TwitchConfig
from chat_thief.command_parser import CommandParser

CONNECTION_DATA = ("irc.chat.twitch.tv", 6667)
ENCODING = "utf-8"
CHAT_MSG = "PRIVMSG"
ARE_YOU_ALIVE = "PING"
I_AM_ALIVE = "PONG"

config = TwitchConfig()


async def pong(server: socket.socket) -> None:
    server.sendall(bytes(I_AM_ALIVE + "\r\n", ENCODING))


def simple_send_msg(server: socket.socket, msg: str) -> None:
    if msg:
        server.sendall(bytes(f"{CHAT_MSG} #{config.channel} :{msg}\n", ENCODING))


async def send_msg(server: socket.socket, msg: str) -> None:
    if msg:
        server.sendall(bytes(f"{CHAT_MSG} #{config.channel} :{msg}\n", ENCODING))


def irc_handshake(server: socket.socket) -> None:
    logger.info(
        json.dumps({"message": f"Connecting to #{config.channel} as {config.bot}"})
    )
    server.sendall(bytes("PASS " + config.token + "\r\n", ENCODING))
    server.sendall(bytes("NICK " + config.bot + "\r\n", ENCODING))
    server.sendall(bytes("JOIN " + f"#{config.channel}" + "\r\n", ENCODING))


async def chat_response(server: socket.socket):
    return server.recv(2048).decode(ENCODING).split()


async def run_bot(server: socket.socket) -> None:
    while True:
        irc_response = await chat_response(server)

        if irc_response[0] == ARE_YOU_ALIVE:
            await pong(server)
        elif len(irc_response) < 2:
            pass
        elif irc_response[1] == CHAT_MSG:
            try:
                if response := CommandParser(irc_response, logger).build_response():
                    MESSAGE_LIMIT = 500

                    if isinstance(response, List):
                        for r in response:
                            await send_msg(server, f"{r}")
                    elif len(response) > MESSAGE_LIMIT:
                        # This is dumb!
                        await send_msg(server, f"{response[:500]}")
                        await send_msg(server, f"{response[500:]}")
                    else:
                        await send_msg(server, f"{response[:500]}")
            except:
                traceback.print_exc()


async def main():
    with socket.socket() as server:
        server.connect(CONNECTION_DATA)
        irc_handshake(server)
        await asyncio.gather(run_bot(server))


if __name__ == "__main__":
    asyncio.run(main())
