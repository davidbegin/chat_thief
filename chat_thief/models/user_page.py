from tinydb import Query  # type: ignore

from chat_thief.models.base_db_model import BaseDbModel


class UserPage(BaseDbModel):
    database_path = "db/user_pages.json"
    table_name = "user_pages"

    @classmethod
    def bootstrap_user_page(cls, user, widgets):
        widget_status = {}
        for widget in widgets:
            widget_status[widget] = True

        return cls(user, widget_status).save()

    # I pass in a list
    # ...then I construct dictionary
    def __init__(self, user, widget_status):
        self._user = user
        self._widget_status = widget_status

    def doc(self):
        return {"user": self._user, "widgets": self._widget_status}

    @classmethod
    def for_user(cls, user):
        return cls.db().get(Query().user == user)

    @classmethod
    def deactivate(cls, user, widget_name):
        cls._change_widget_status(user, widget_name, False)

    @classmethod
    def activate(cls, user, widget_name):
        cls._change_widget_status(user, widget_name, True)

    @classmethod
    def _change_widget_status(cls, user, widget_name, status):
        user_page = cls.db().get(Query().user == user)

        if user_page is None:
            print(f"Could Not Find User Page: {user} - Bootstrapping")

            cls.bootstrap_user_page(user, [widget_name])
            user_page = cls.db().get(Query().user == user)

        if "widgets" in user_page:
            user_page["widgets"][widget_name] = status
            UserPage.set_value_by_id(user_page.doc_id, "widgets", user_page["widgets"])
