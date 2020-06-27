from chat_thief.models.user import User


class Result:
    def __init__(self, user, command, metadata):
        self.user = user
        self.command = command
        self.metadata = metadata
        self._set_cool_points_diff()

    def _set_cool_points_diff(self):
        if "purchase_results" in self.metadata:
            total_spent = sum(
                [result.cost for result in self.metadata["purchase_results"]]
            )
            self.cool_points_diff = -total_spent
        else:
            self.cool_points_diff = 0
