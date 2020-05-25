from chat_thief.models.base_db_model import BaseDbModel


class Notification(BaseDbModel):
    table_name = "notifications"
    database_path = "db/notifications.json"

    def __init__(self, message, duration=1):
        self.message = message
        self.duration = duration

    def doc(self):
        return {"message": self.message, "duration": self.duration}
