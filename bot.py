import json
import logging
import os
import socket
import sys
import time
from pathlib import Path
from logging.handlers import RotatingFileHandler

# socket()
# connect()
# send()

# Why am I never closing
# should I be passing the server object around

ENCODING="utf-8"
CHAT_MSG="PRIVMSG"
ARE_YOU_ALIVE="PING"
I_AM_ALIVE="PONG"

def send_msg(msg):
    server = connect_to_twitch()

    # We want all configuration pulled out and validated
    channel = os.environ.get("TWITCH_CHANNEL", "beginbot")

    if msg:
        result = server.sendall(
            bytes(f"{CHAT_MSG} #{channel} :{msg}\n", ENCODING)
        )

def run_bot(server):
    # Too much logging logic
    logger = logging.getLogger("Chat Log")
    logger.setLevel(logging.INFO)
    Path("logs").mkdir(exist_ok=True)
    # Decide what I want around logging
    handler = RotatingFileHandler("logs/chat.log", maxBytes=50000000, backupCount=5)
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    
    while True:
        # Why do I use the magical 2048
        irc_response = server.recv(2048).decode(ENCODING).split()

        if irc_response[1] == CHAT_MSG:
            user, msg = _parse_user_and_msg(irc_response)
            logger.info(f"{user}: {msg}")
        elif irc_response[0] == ARE_YOU_ALIVE:
            server.sendall(bytes(I_AM_ALIVE + "\r\n", ENCODING))


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

    # Is this the 3-Way Client Handshake
    # Is this IRC only?
    server.sendall(bytes("PASS " + token + "\r\n", ENCODING))
    server.sendall(bytes("NICK " + bot + "\r\n", ENCODING))
    server.sendall(bytes("JOIN " + f"#{channel}" + "\r\n", ENCODING))

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

    connection_data = ("irc.chat.twitch.tv", 6667)
    # AF_INET and SOCK_STREAM
    with socket.socket() as server:
        server.connect(connection_data)
        _handshake(server)
        run_bot(server)
