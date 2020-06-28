from tinydb import Query

from chat_thief.models.base_db_model import BaseDbModel


class UserCode(BaseDbModel):
    database_path = "db/user_code.json"
    table_name = "user_code"

    def __init__(self, user, code_link, code_type):
        self.user = user
        self.code_link = code_link
        self.code_type = code_type

    def doc(self):
        return {
            "user": self.user,
            "code_link": self.code_link,
            "code_type": self.code_type,
        }
