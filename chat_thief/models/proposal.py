from tinydb import Query
from datetime import datetime
import time

from chat_thief.models.base_db_model import BaseDbModel


class Proposal(BaseDbModel):
    table_name = "proposals"
    database_path = "db/proposals.json"

    def __init__(self, user, command, proposal):
        self.user = user
        self.command = command
        self.proposal = proposal
        self.supporters = []

    @classmethod
    def support(cls, user, doc_id, supporter):
        def add_support(supporter):
            def transform(doc):
                if supporter not in doc["supporters"]:
                    doc["supporters"].append(supporter)

            return transform

        cls.db().update(add_support(supporter), doc_ids=[doc_id])
        return f"@{user} thanks you for the support @{supporter}"

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
