from pathlib import Path
import re
import itertools
import operator

from tinydb import Query  # type: ignore

from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.user_page import UserPage


class UserCode(BaseDbModel):
    database_path = "db/user_code.json"
    table_name = "user_code"

    def __init__(
        self, user, code_link, code_type, name=None, approved=False, owners=[]
    ):
        self._user = user
        self._code_link = code_link
        self._code_type = code_type
        self._approved = approved
        self._owners = owners
        if name:
            self._name = name
        else:
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

    def upsert_doc(self):
        return {
            "user": self._user,
            "name": self._name,
            "code_link": self._code_link,
            "code_type": self._code_type,
        }

    def update_or_create(self):
        self.db().upsert(
            self.upsert_doc(),
            (Query().name == self._name) & (Query().user == self._user),
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
        user_code = cls.db().get(Query().name.matches(widget_name, flags=re.IGNORECASE))
        if user_code:
            owners = user_code.get("owners", [])

            if purchaser not in owners:
                owners.append(purchaser)
                cls.set_value_by_id(user_code.doc_id, "owners", owners)
                return (
                    f"@{purchaser} bought {widget_name}.js from @{user_code['user']}!"
                )
            else:
                return f"@{cls.purchaser} already owners {widget_name}!"
        else:
            return f"Could Not Find {widget_name} to purchase"

    @classmethod
    def find_owners(cls, widget_name):
        user_code = cls.db().get(Query().name.matches(widget_name, flags=re.IGNORECASE))
        if user_code:
            return [user_code["user"]] + user_code["owners"]

    @classmethod
    def owned_by(cls, user):
        directly_owned = cls.db().search((Query().user == user))

        def is_owner(user_code):
            return user_code["approved"] and user in user_code.get("owners", [])

        results = cls.db().search(is_owner)
        return [f"{result['name']}.js" for result in (results + directly_owned)]

    @classmethod
    def dev_leaderboard(cls):
        results = {}
        for user_code in cls.all():
            user_name = user_code["user"]

            if user_name in results:
                results[user_name] += len(user_code["owners"])
            else:
                results[user_name] = len(user_code["owners"])

        owned = [(user, owner_count) for (user, owner_count) in results.items()]
        return list(reversed(sorted(owned, key=lambda user_widgets: user_widgets[1])))

    # We need to check UserPage Status
    @classmethod
    def js_for_user(cls, user):
        def is_owned_by(user_code):
            return user in user_code.get("owners", []) or user_code["user"] == user

        results = cls.db().search(is_owned_by)
        owned_by = {"approved": [], "unapproved": [], "deactivated": []}

        for result in results:
            if result.get("approved", False):
                owned_by["approved"].append(f"{result['name']}.js")
            else:
                owned_by["unapproved"].append(f"{result['name']}.js")

        user_page = UserPage.for_user(user)
        if user_page:
            widgets = user_page["widgets"]
            if widgets:
                deactivated = [
                    f"{widget}.js" for (widget, active) in widgets.items() if not active
                ]
            owned_by["deactivated"] = deactivated
        return owned_by
