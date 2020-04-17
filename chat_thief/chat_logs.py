from pathlib import Path
from collections import Counter

from chat_thief.stream_lords import STREAM_GODS


# How do we get more recent users???
class ChatLogs:
    def __init__(self):
        lines = self._read_in_chat(all_lines=True)
        self.raw_users = [chat_msg.split(":")[0] for chat_msg in lines]

    def users(self):
        return list(set(self.raw_users))

    def most_msgs(self):
        return Counter(self.raw_users)

    def recent_stream_peasants(self):
        lines = self._read_in_chat(line_count=10)
        return list(
            set(
                [
                    chat_msg.split(":")[0]
                    for chat_msg in lines
                    if chat_msg.split(":")[0] not in STREAM_GODS
                ]
            )
        )

    def _read_in_chat(self, line_count=50, all_lines=False):
        with Path(__file__).parent.parent.joinpath("logs/chat.log") as log:
            chat_lines = [line for line in log.read_text().split("\n") if line]
            if all_lines:
                lines = chat_lines
            else:
                lines = chat_lines[-line_count:]
        return lines
