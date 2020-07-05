from tinydb import Query  # type: ignore
from datetime import datetime
import time

from chat_thief.models.base_db_model import BaseDbModel

DEFAULT_EXPIRE_TIME_IN_SECS = 300


class Proposal(BaseDbModel):
    table_name = "proposals"
    database_path = "db/proposals.json"
    EXPIRE_TIME_IN_SECS = DEFAULT_EXPIRE_TIME_IN_SECS

    # A User can only have one proposal at a time
    # If they make a new one, it overwrites the old one
    # and resets the time frame for approval
    def __init__(self, user, command=None, proposal=None):
        self.user = user
        self.command = command
        self.proposal = proposal
        self.supporters = []

    def is_expired(self):
        info = self.db().get(Query().user == self.user)

        if info:
            current_time = datetime.fromtimestamp(time.time())
            proposed_at = datetime.fromisoformat(info["proposed_at"])
            elapsed_time = current_time - proposed_at
            return elapsed_time.seconds >= self.EXPIRE_TIME_IN_SECS
        else:
            # If we can't find the proposal, then assume
            # it is expired
            return True

    @classmethod
    def support_last(cls, supporter):
        last_proposal = cls.last()
        return cls.support(last_proposal["user"], last_proposal.doc_id, supporter)

    @classmethod
    def support(cls, user, doc_id, supporter):
        if user == supporter:
            return f"Can't support yourself @{supporter}"

        supporters = cls.db().get(doc_id=doc_id)["supporters"]
        if supporter in supporters:
            return f"You already supported! @{supporter}"

        def add_support(supporter):
            def transform(doc):
                if supporter not in doc["supporters"]:
                    doc["supporters"].append(supporter)

            return transform

        cls.db().update(add_support(supporter), doc_ids=[doc_id])
        return f"@{user} Thanks You for the support @{supporter}"

    @classmethod
    def find_by_user(cls, user):
        return cls.db().get(Query().user == user)

    def doc(self):
        proposed_at = str(datetime.fromtimestamp(time.time()))

        return {
            "user": self.user,
            "command": self.command,
            "proposal": self.proposal,
            "supporters": self.supporters,
            "proposed_at": proposed_at,
        }
