from tinydb import Query

from chat_thief.models.base_db_model import BaseDbModel


class UserCode(BaseDbModel):
    database_path = "db/user_code.json"
    table_name = "user_code"

    def __init__(self, user, code_link, code_type, approved=False):
        self._user = user
        self._code_link = code_link
        self._code_type = code_type
        self._approved = approved

    def doc(self):
        return {
            "user": self._user,
            "code_link": self._code_link,
            "code_type": self._code_type,
            "approved": self._approved,
        }
