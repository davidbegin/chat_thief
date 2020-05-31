from optparse import OptionParser

from pathlib import Path
import re
import string
import sys
import codecs

from typing import List

DEFAULT_LINES_TO_GRAB = 5
# BLACKLISTED_USERS = ["beginbotbot", "nightbot"]
# BLACKLISTED_USERS = []
BLACKLISTED_USERS = ["nightbot"]

DICT_WORDS = Path("/usr/share/dict/cracklib-small").read_text().split()


def filter_out_logs(logs: List[str]) -> List[str]:
    pattern = re.compile("[^{]*: .*")
    return [
        log
        for log in logs
        if pattern.match(log) and log.split(":")[0] not in BLACKLISTED_USERS
    ]


def rot13(text: str) -> str:
    decrypted_msg, _length = codecs.lookup("rot13").encode(text)
    return decrypted_msg


# Identify URLs and ping them first?
# or just regular
#
# This fails for code
def is_encrypted_msg(line: str) -> bool:
    chat_words = [word for word in line.split(" ")[1:] if word.strip()]

    regular_word_matches = len(set(DICT_WORDS) & set(chat_words))
    rot13_word_matches = len(
        set(DICT_WORDS) & set([rot13(word) for word in chat_words])
    )
    return rot13_word_matches > regular_word_matches


def decrypt_msg(line: str) -> str:
    if is_encrypted_msg(line):
        chat_words = [word for word in line.split(" ") if word.strip()]
        username, *words = chat_words
        return f"*{username}* {' '.join([rot13(word) for word in words ])}"
    else:
        return line


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

        # We should do something when there are less lines than the count
        # chat = [decrypt_msg(msg) for msg in filter_out_logs(lines)]
        chat = lines

    print("\n".join(chat))
