import socket

import sys

from bot import irc_handshake, simple_send_msg, CONNECTION_DATA

# We add ! to these commands
NIGHTBOT_COMMANDS = [
    "discord",
    "github",
    "links",
    "linux",
    "guest",
    "marker",
    "schedule",
    "so",
    "idk",
    "ha",
    "wyp",
    "jdi",
    "clap",
    "ahh",
    "topic",
]

if __name__ == "__main__":
    with socket.socket() as server:
        server.connect(CONNECTION_DATA)
        irc_handshake(server)
        cmd, *args = sys.argv[1:]

        # This should look for this commands when I am sending them and add the exclamation if I have a sound effect
        if cmd in NIGHTBOT_COMMANDS:
            cmd = f"!{cmd}"

        try:
            simple_send_msg(server, f"{cmd} {' '.join(args)}")
        except Exception as e:
            print(e)
