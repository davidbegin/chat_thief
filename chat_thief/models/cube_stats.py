
from chat_thief.models.base_db_model import BaseDbModel


class CubeStats(BaseDbModel):
    table_name = "cube_stats"
    database_path = "db/cube_stats.json"

    def __init__(self):
        pass
