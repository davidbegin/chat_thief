from pathlib import Path
import re
import sys

DEFAULT_LINES_TO_GRAB = 5
LINES_TO_GRAB = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LINES_TO_GRAB
BLACKLISTED_USERS = []
# BLACKLISTED_USERS = ["beginbotbot"]

def filter_out_logs(logs):
    pattern = re.compile("[^{]*: .*")
    return [
        log
        for log in logs
        if pattern.match(log) and log.split(":")[0] not in BLACKLISTED_USERS
    ]


# Path(__file__).parent.joinpath("logs/chat.log")
with Path(__file__).parent.joinpath("logs/chat.log") as log:
# with Path("logs/chat.log") as log:
    chat_lines = log.read_text().split("\n")
    chat = filter_out_logs(chat_lines[-LINES_TO_GRAB:])
    print("\n".join(chat))
