import socket
import sys

from bot import irc_handshake, send_msg, CONNECTION_DATA

# We add ! to these commands
NIGHTBOT_COMMANDS = [
    "discord",
    "github",
    "links",
    "marker",
    "schedule",
    "so",
    "topic",
]

if __name__ == "__main__":
    with socket.socket() as server:
        server.connect(CONNECTION_DATA)
        irc_handshake(server)
        cmd, *args = sys.argv[1:]
        if cmd in NIGHTBOT_COMMANDS:
            cmd = f"!{cmd}"

        send_msg(server, f"{cmd} {' '.join(args)}")
