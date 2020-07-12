from typing import List, Dict
import json
import socket
import asyncio
import traceback

from chat_thief.config.log import logger
from chat_thief.config.twitch import TwitchConfig
from chat_thief.command_router import CommandRouter

BEGINBOTBOT = ":beginbotbot!beginbotbot@beginbotbot.tmi.twitch.tv"
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
    logger.debug(
        json.dumps({"message": f"Connecting to #{config.channel} as {config.bot}"})
    )
    server.sendall(bytes("PASS " + config.token + "\r\n", ENCODING))
    server.sendall(bytes("NICK " + config.bot + "\r\n", ENCODING))
    server.sendall(bytes("JOIN " + f"#{config.channel}" + "\r\n", ENCODING))


async def chat_response(server: socket.socket):
    # whatsinmyopsec: so i can be a web dever :beginbotbot!beginbotbot@beginbotbot.tmi.twitch.tv PRIVMSG #beginbot :@lunchboxsushi now has access to !myspacepage :beginbotbot!beginbotbot@beginbotbot.tmi.twitch.tv PRIVMSG #beginbot :Welcome @lunchboxsushi! You need a Theme song (max 5 secs): !soundeffect YOUTUBE-URL @lunchboxsushi 00:03 00:07
    # So I typically splitting on whitespace.
    # return server.recv(2048).decode(ENCODING).split()
    return server.recv(2048).decode(ENCODING)


async def run_bot(server: socket.socket) -> None:
    while True:
        raw_irc_response = await chat_response(server)
        # Example:
        #   :beginbotbot!beginbotbot@beginbotbot.tmi.twitch.tv PRIVMSG #beginbot :!wildcard

        if ARE_YOU_ALIVE in raw_irc_response:
            await pong(server)
        elif len(raw_irc_response.split()) < 2:
            pass
        elif CHAT_MSG in raw_irc_response:
            if raw_irc_response.startswith(BEGINBOTBOT):
                irc_response = raw_irc_response
            else:
                irc_response = raw_irc_response.split(BEGINBOTBOT)[0].strip()

            # I think sometimes the messages can still end up on one line
            # However I haven't found an example yet
            # print(f"{irc_response=}")

            try:
                if response := CommandRouter(irc_response, logger).build_response():
                    MESSAGE_LIMIT = 500

                    if isinstance(response, List):
                        for r in response:
                            await send_msg(server, f"{r}")
                    elif len(response) > MESSAGE_LIMIT:
                        # This is dumb!
                        await send_msg(server, f"{response[:500]}")
                        await send_msg(server, f"{response[500:]}")
                    else:
                        await send_msg(server, f"{response}")
            except:
                print("\033[91m")
                traceback.print_exc()
                print("\033[0m")


async def main():
    with socket.socket() as server:
        server.connect(CONNECTION_DATA)
        irc_handshake(server)
        await asyncio.gather(run_bot(server))


if __name__ == "__main__":
    asyncio.run(main())
