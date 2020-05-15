from chat_thief.models.base_db_model import BaseDbModel
from datetime import datetime
import time


class BreakingNews(BaseDbModel):
    table_name = "breaking_news"
    database_path = "db/breaking_news.json"

    def __init__(self, scope, user=None):
        self._scope = scope
        self._user = user

    def doc(self):
        scope_time = datetime.fromtimestamp(time.time())
        return {"scope": self._scope, "user": self._user, "timestamp": str(scope_time)}
