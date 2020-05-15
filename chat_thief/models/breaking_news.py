from chat_thief.models.base_db_model import BaseDbModel
from datetime import datetime
import time


class BreakingNews(BaseDbModel):
    table_name = "breaking_news"
    database_path = "db/breaking_news.json"

    def __init__(
        self,
        scope,
        user=None,
        category=None,
        revolutionaries=[],
        peace_keepers=[],
        fence_sitters=[],
    ):
        self._scope = scope
        self._user = user
        self._category = category
        self._revolutionaries = revolutionaries
        self._peace_keepers = peace_keepers
        self._fence_sitters = fence_sitters

    def doc(self):
        scope_time = datetime.fromtimestamp(time.time())
        return {
            "scope": self._scope,
            "user": self._user,
            "category": self._category,
            "timestamp": str(scope_time),
            "revolutionaries": self._revolutionaries,
            "peace_keepers": self._peace_keepers,
            "fence_sitters": self._fence_sitters,
        }
