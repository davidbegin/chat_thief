from datetime import datetime
import time

from chat_thief.models.base_db_model import BaseDbModel


class UserEvent(BaseDbModel):
    table_name = "user_events"
    database_path = "db/user_events.json"

    def __init__(self, user, command, msg, result):
        self._user = user
        self._command = command
        self._msg = msg
        self._result = result

    def doc(self):
        created_at = str(datetime.fromtimestamp(time.time()))

        return {
            "user": self._user,
            "command": self._command,
            "msg": self._msg,
            "result": self._result,
            "created_at": created_at,
        }
