from pathlib import Path
from collections import Counter

from chat_thief.config.stream_lords import STREAM_GODS

# Keeping to shorter number rewards more recent users,
# ALL_LINES has to also be False
DEFAULT_LINE_COUNT = 1000
ALL_LINES = True


class ChatLogs:
    def __init__(self):
        lines = self._read_in_chat(all_lines=True)
        self.raw_users = [chat_msg.split(":")[0] for chat_msg in lines]

    def users(self):
        return list(set(self.raw_users))

    def most_msgs(self):
        return Counter(self.raw_users)

    def recent_stream_peasants(self):
        lines = self._read_in_chat(line_count=DEFAULT_LINE_COUNT, all_lines=False)
        users = [chat_msg.split(":")[0].strip() for chat_msg in lines]
        # peasants = [user for user in users if user not in STREAM_GODS]
        peasants = list(set([user for user in users if user not in STREAM_GODS]))

        return peasants

    def _read_in_chat(self, line_count=DEFAULT_LINE_COUNT, all_lines=ALL_LINES):
        with Path(__file__).parent.parent.joinpath("logs/chat.log") as log:
            chat_lines = [line for line in log.read_text().split("\n") if line]
            if all_lines:
                lines = chat_lines
            else:
                lines = chat_lines[-line_count:]
        return lines
