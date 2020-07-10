from typing import Optional, List, Any, Dict

import time

from chat_thief.models.base_db_model import BaseDbModel
from datetime import datetime

from tinydb import Query  # type: ignore
from tinydb.table import Document  # type: ignore


class BreakingNews(BaseDbModel):
    table_name = "breaking_news"
    database_path = "db/breaking_news.json"

    def __init__(
        self,
        scope: str,
        user: Optional[str] = None,
        category: Optional[str] = None,
        reported_on: Optional[bool] = False,
        revolutionaries: Optional[List[str]] = [],
        peace_keepers: Optional[List[str]] = [],
        fence_sitters: Optional[List[str]] = [],
    ):
        self._scope = scope
        self._user = user
        self._category = category
        self._reported_on = reported_on
        self._revolutionaries = revolutionaries
        self._peace_keepers = peace_keepers
        self._fence_sitters = fence_sitters

    @classmethod
    def unreported_news(cls) -> Optional[Document]:
        return cls.db().get(Query().reported_on == False)

    @classmethod
    def report_last_story(cls) -> Optional[Document]:
        last_story = cls.unreported_news()
        if last_story:
            cls.set_value_by_id(last_story.doc_id, "reported_on", True)
            return last_story
        else:
            return None

    def doc(self) -> Dict:
        scope_time = datetime.fromtimestamp(time.time())
        return {
            "scope": self._scope,
            "user": self._user,
            "category": self._category,
            "timestamp": str(scope_time),
            "reported_on": self._reported_on,
            "revolutionaries": self._revolutionaries,
            "peace_keepers": self._peace_keepers,
            "fence_sitters": self._fence_sitters,
        }
