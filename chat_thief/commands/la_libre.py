from chat_thief.chat_logs import ChatLogs
from chat_thief.models.command import Command
from chat_thief.models.user import User
from chat_thief.models.vote import Vote

REVOLUTION_LIKELYHOOD = 14


class LaLibre:

    # Total Number of Votes
    # Peace and Revolution Break Down
    # Coup Costs
    # Potential Revolutionaries
    @classmethod
    def inform(cls):
        peasants = ChatLogs().recent_stream_peasants()
        threshold = int(len(peasants) / REVOLUTION_LIKELYHOOD)

        if threshold < 3:
            threshold = 3

        return [
            "PowerUpL La Libre PowerUpR",
            f"Total Votes: {Vote.count()}",
            f"Peace Count: {Vote.peace_count()} / {threshold}",
            f"Revolution Count: {Vote.revolution_count()} / {threshold}",
            f"panicBasket Coup Cost: {Command('coup').cost()} panicBasket",
        ]
