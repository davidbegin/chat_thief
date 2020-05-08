from chat_thief.models.vote import Vote
from chat_thief.models.command import Command
from chat_thief.models.user import User


class LaLibre:

    # Total Number of Votes
    # Peace and Revolution Break Down
    # Coup Costs
    # Potential Revolutionaries
    @classmethod
    def inform(cls):
        threshold = int(User.count() / 10)

        return [
            "PowerUpL La Libre PowerUpR",
            f"Total Votes: {Vote.count()}",
            f"Peace Count: {Vote.peace_count()}",
            f"Revolution Count: {Vote.revolution_count()}",
            f"Votes Required: {threshold}",
            f"panicBasket Coup Cost: {Command('coup').cost()} panicBasket",
        ]
