from chat_thief.models.base_db_model import BaseDbModel
from datetime import datetime
import time


class BreakingNews(BaseDbModel):
    table_name = "breaking_news"
    database_path = "db/breaking_news.json"

    def __init__(self, scope):
        self._scope = scope

    def doc(self):
        # datetime.utcnow()
        # datetime.utcnow()

        scope_time = datetime.fromtimestamp(time.time())
        return {"scope": self._scope, "timestamp": str(scope_time)}
