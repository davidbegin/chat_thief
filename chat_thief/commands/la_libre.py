from typing import List

from chat_thief.chat_logs import ChatLogs
from chat_thief.models.command import Command
from chat_thief.models.user import User
from chat_thief.models.vote import Vote

REVOLUTION_LIKELYHOOD = 14
DEFAULT_THRESHOLD = 3


class LaLibre:
    @classmethod
    def threshold(cls) -> int:
        peasants = ChatLogs().recent_stream_peasants()
        value = int(len(peasants) / REVOLUTION_LIKELYHOOD)
        if value < DEFAULT_THRESHOLD:
            return DEFAULT_THRESHOLD
        return value

    @classmethod
    def inform(cls) -> List[str]:
        return [
            "PowerUpL La Libre PowerUpR",
            f"Total Votes: {Vote.count()}",
            f"Peace Count: {Vote.peace_count()} / {cls.threshold()}",
            f"Revolution Count: {Vote.revolution_count()} / {cls.threshold()}",
            f"panicBasket Coup Cost: {Command('coup').cost()} panicBasket",
        ]
