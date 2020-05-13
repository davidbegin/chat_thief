from chat_thief.models.base_db_model import BaseDbModel


# Base Model, should throw error if you don't
# Make this an ABV
class Issue(BaseDbModel):
    table_name = "issues"
    database_path = "db/issues.json"

    def __init__(self, user, msg):
        self._user = user
        self._msg = msg

    def save(self):
        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.insert(self.doc())

    def doc(self):
        return {"user": self._user, "msg": self._msg}
