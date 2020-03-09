import json
import logging
import os
import socket
import sys
import time
from pathlib import Path
from logging.handlers import RotatingFileHandler


def send_msg(msg):
    server = connect_to_twitch()
    channel = os.environ.get("TWITCH_CHANNEL", "beginbot")

    if msg:
        result = server.send(
            bytes("PRIVMSG " + f"#{channel}" + " :" + msg + "\n", "utf-8")
        )

def run_bot(server):
    logger = logging.getLogger("Chat Log")
    logger.setLevel(logging.INFO)
    Path("logs").mkdir(exist_ok=True)
    handler = RotatingFileHandler("logs/chat.log", maxBytes=50000000, backupCount=5)
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    
    while True:
        irc_response = server.recv(2048).decode("utf-8").split()

        if irc_response[1] == "PRIVMSG":
            user, msg = _parse_user_and_msg(irc_response)
            logger.info(f"{user}: {msg}")
        elif irc_response[0] == "PING":
            server.send(bytes("PONG" + "\r\n", "utf-8"))


def _parse_user_and_msg(irc_response):
    user_info, _, _, *raw_msg = irc_response
    raw_first_word, *raw_rest_of_the_message = raw_msg
    first_word = raw_first_word[1:]
    rest_of_the_message = " ".join(raw_rest_of_the_message)
    user = user_info.split("!")[0][1:]
    msg = f"{first_word} {rest_of_the_message}"
    return user, msg


def _is_command_msg(msg):
    return msg[0] == "!" and msg[1] != "!"

def _handshake(server):
    token = os.environ["TWITCH_OAUTH_TOKEN"]
    bot = os.environ["TWITCH_BOT_NAME"]
    channel = os.environ.get("TWITCH_CHANNEL", "beginbot")

    print(json.dumps({"message": f"Connecting to #{channel} as {bot}"}))

    server.send(bytes("PASS " + token + "\r\n", "utf-8"))
    server.send(bytes("NICK " + bot + "\r\n", "utf-8"))
    server.send(bytes("JOIN " + f"#{channel}" + "\r\n", "utf-8"))

def connect_to_twitch():
    connection_data = ("irc.chat.twitch.tv", 6667)
    server = socket.socket()
    server.connect(connection_data)
    _handshake(server)
    return server


if __name__ == "__main__":
    required_config = "TWITCH_OAUTH_TOKEN TWITCH_CHANNEL TWITCH_BOT_NAME"
    errors = [
        f"Missing environment variable: {var}"
        for var in required_config.split()
        if var not in os.environ
    ]
    if errors:
        print(errors)
        raise ValueError(errors)

    server = connect_to_twitch()
    run_bot(server)
