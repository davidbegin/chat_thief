from chat_thief.models.base_db_model import BaseDbModel


class Issue(BaseDbModel):
    table_name = "issues"
    database_path = "db/issues.json"

    def __init__(self, user, msg):
        self._user = user
        self._msg = msg

    def doc(self):
        return {"user": self._user, "msg": self._msg}
