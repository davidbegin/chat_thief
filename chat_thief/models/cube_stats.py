from chat_thief.models.base_db_model import BaseDbModel


class CubeStats(BaseDbModel):
    table_name = "cube_stats"
    database_path = "db/cube_stats.json"

    def __init__(self, winning_duration, winners, all_bets):
        self._winning_duration = winning_duration
        self._winners = winners
        self._all_bets = all_bets

    def doc(self):
        formatted_bets = [{"user": bet[0], "bet": bet[1]} for bet in self._all_bets]

        return {
            "winning_duration": self._winning_duration,
            "winners": self._winners,
            "all_bets": formatted_bets,
        }
