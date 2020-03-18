from optparse import OptionParser
from pathlib import Path
import re
import string
import sys

from typing import List

DEFAULT_LINES_TO_GRAB = 5
# BLACKLISTED_USERS = ["beginbotbot", "nightbot"]
BLACKLISTED_USERS = ["nightbot"]
# BLACKLISTED_USERS = []


def filter_out_logs(logs: List[str]) -> List[str]:
    pattern = re.compile("[^{]*: .*")
    return [
        log
        for log in logs
        if pattern.match(log) and log.split(":")[0] not in BLACKLISTED_USERS
    ]


def rot13(text: str) -> str:
    abc = string.ascii_lowercase
    return "".join([abc[(abc.find(c) + 13) % 26] for c in text])


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        "-c",
        "--count",
        type=int,
        dest="line_count",
        default=DEFAULT_LINES_TO_GRAB,
        help="write report to FILE",
    )
    parser.add_option(
        "-a",
        "--all",
        action="store_true",
        dest="all",
        default=False,
        help="don't print status messages to stdout",
    )
    (options, args) = parser.parse_args()

    with Path(__file__).parent.joinpath("logs/chat.log") as log:
        chat_lines = [line for line in log.read_text().split("\n") if line]
        if options.all:
            lines = chat_lines
        else:
            lines = chat_lines[-options.line_count :]

        dict_words = Path("/usr/share/dict/cracklib-small").read_text().split()
        for line in lines:
            chat_words = [word for word in line.split(" ") if word]
            regular_word_matches = len(set(dict_words) & set(chat_words))
            rot13_word_matches = len(
                set(dict_words) & set([rot13(word) for word in chat_words])
            )

            # We need some spell checking
            if rot13_word_matches > regular_word_matches and rot13_word_matches > 0:
                username, *words = chat_words
                print(f"{rot13(username)} {' '.join(words)}")

        chat = filter_out_logs(lines)
    print("\n".join(chat))
