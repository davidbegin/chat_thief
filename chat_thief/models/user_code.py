from pathlib import Path

from tinydb import Query

from chat_thief.models.base_db_model import BaseDbModel


class UserCode(BaseDbModel):
    database_path = "db/user_code.json"
    table_name = "user_code"

    def __init__(self, user, code_link, code_type, approved=False, owners=[]):
        self._user = user
        self._code_link = code_link
        self._code_type = code_type
        self._approved = approved
        self._owners = owners
        self._name = Path(code_link).name[:-3]

    def doc(self):
        return {
            "user": self._user,
            "name": self._name,
            "owners": self._owners,
            "code_link": self._code_link,
            "code_type": self._code_type,
            "approved": self._approved,
        }

    @classmethod
    def purchase(cls, purchaser, widget_name):
        user_code = cls.db().get(Query().name == widget_name)
        owners = user_code["owners"]

        if purchaser not in owners:
            owners.append(purchaser)
            cls.set_value_by_id(user_code.doc_id, "owners", owners)
        else:
            return f"@{cls.purchaser} already owners {widget_name}!"

    @classmethod
    def find_owners(cls, widget_name):
        user_code = cls.db().get(Query().name == widget_name)
        return [user_code["user"]] + user_code["owners"]

    @classmethod
    def owned_by(cls, user):
        # Created By a User
        results = cls.db().search(Query().user == user)
        return [f"{result['name']}.js" for result in results]
