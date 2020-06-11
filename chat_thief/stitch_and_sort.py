from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.user import User
from chat_thief.models.command import Command


class StitchAndSort:

    def __init__(self):
        votes = SFXVote.db().all()
        users = User.db().all()
        commands = Command.db().all()

    def stiched_and_sort(self):
        pass
