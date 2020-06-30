from tinydb import Query

from chat_thief.models.base_db_model import BaseDbModel


class UserPage(BaseDbModel):
    database_path = "db/user_pages.json"
    table_name = "user_pages"

    def __init__(self, user, widgets=[]):
        self._user = user
        self._widgets = widgets

        self.widget_status = {}
        for widget in widgets:
            self.widget_status[widget] = True

    def doc(self):
        return {"user": self._user, "widgets": self.widget_status}

    @classmethod
    def for_user(cls, user):
        return cls.db().get(Query().user == user)

    @classmethod
    def deactivate(cls, user, widget_name):
        user_page = cls.db().get(Query().user == user)

        if user_page is None:
            return f"No widget found to deactivate: {widget_name}"

        if "widgets" in user_page:
            if widget_name in user_page["widgets"]:
                user_page["widgets"][widget_name] = False
                UserPage.set_value_by_id(
                    user_page.doc_id, "widgets", user_page["widgets"]
                )
