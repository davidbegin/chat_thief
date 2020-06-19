from chat_thief.models.base_db_model import BaseDbModel


class RapSheet(BaseDbModel):
    database_path = "db/rap_sheet.json"
    table_name = "rap_sheet"

    def __init__(self, user, action, metadata={}):
        self._user = user
        self._action = action
        self._metadata = metadata

    def doc(self):
        return {"user": self._user, "action": self._action, "metadata": self._metadata}
