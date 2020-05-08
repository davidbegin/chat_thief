from chat_thief.models.vote import Vote
from chat_thief.models.command import Command
from chat_thief.models.user import User

REVOLUTION_LIKELYHOOD = 14


class LaLibre:

    # Total Number of Votes
    # Peace and Revolution Break Down
    # Coup Costs
    # Potential Revolutionaries
    @classmethod
    def inform(cls):
        threshold = int(User.count() / REVOLUTION_LIKELYHOOD)

        return [
            "PowerUpL La Libre PowerUpR",
            f"Total Votes: {Vote.count()}",
            f"Peace Count: {Vote.peace_count()} / {threshold}",
            f"Revolution Count: {Vote.revolution_count()} / {threshold}",
            f"panicBasket Coup Cost: {Command('coup').cost()} panicBasket",
        ]
