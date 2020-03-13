from pathlib import Path
import re
import sys

DEFAULT_LINES_TO_GRAB = 5
BLACKLISTED_USERS = []
# BLACKLISTED_USERS = ["beginbotbot"]

from optparse import OptionParser


def filter_out_logs(logs):
    pattern = re.compile("[^{]*: .*")
    return [
        log
        for log in logs
        if pattern.match(log) and log.split(":")[0] not in BLACKLISTED_USERS
    ]


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--count", dest="line_count", default=DEFAULT_LINES_TO_GRAB,
                      help="write report to FILE")
    parser.add_option("-a", "--all",
                      action="store_true", dest="all", default=False,
                      help="don't print status messages to stdout")
    (options, args) = parser.parse_args()

    with Path(__file__).parent.joinpath("logs/chat.log") as log:
        chat_lines = log.read_text().split("\n")
        if options.all:
            lines = chat_lines
        else:
            lines = chat_lines[-options.line_count:]
        chat = filter_out_logs(lines)
    print("\n".join(chat))
