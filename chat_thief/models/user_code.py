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
        if code_link.endswith(".js"):
            self._name = Path(code_link).name[:-3]
        else:
            self._name = self._user

    def doc(self):
        return {
            "user": self._user,
            "name": self._name,
            "owners": self._owners,
            "code_link": self._code_link,
            "code_type": self._code_type,
            "approved": self._approved,
        }

    def update_or_create(self):
        self.db().upsert(
            self.doc(), (Query().name == self._name) & (Query().user == self._user)
        )
        return self

    @classmethod
    def approve(cls, user, widget_name=None):
        if user:
            result = cls.db().get(Query().user == user)
            cls.set_value_by_id(result.doc_id, "approved", True)
            return f"@{result['user']}'s {result['name']}.js has been approved!"

        result = cls.db().get(Query().name == widget_name)
        if result:
            cls.set_value_by_id(result.doc_id, "approved", True)
            return f"@{result['user']}'s {result['name']}.js has been approved!"

        return f"Could Not Find User Code to Approve {self.args}"

    @classmethod
    def purchase(cls, purchaser, widget_name):
        user_code = cls.db().get(Query().name == widget_name)
        owners = user_code["owners"]

        if purchaser not in owners:
            owners.append(purchaser)
            cls.set_value_by_id(user_code.doc_id, "owners", owners)
            return f"@{purchaser} bought {widget_name}.js from @{user_code['user']}!"
        else:
            return f"@{cls.purchaser} already owners {widget_name}!"

    @classmethod
    def find_owners(cls, widget_name):
        user_code = cls.db().get(Query().name == widget_name)
        return [user_code["user"]] + user_code["owners"]

    @classmethod
    def owned_by(cls, user):
        directly_owned = cls.db().search(
            (Query().user == user) & (Query().approved == True)
        )

        def is_owner(user_code):
            return user in user_code.get("owners", [])

        results = cls.db().search(is_owner)
        return [f"{result['name']}.js" for result in (results + directly_owned)]
