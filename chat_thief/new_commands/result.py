from chat_thief.models.user import User, PurchaseResult


class Result:
    def __init__(self, user, command, results):
        self.user = user
        self.command = command
        self.results = results
        self._set_cool_points_diff()

    def _set_cool_points_diff(self):
        total_spent = sum(
            [
                result.cost
                for result in self.results
                if isinstance(result.result, PurchaseResult)
            ]
        )
        self.cool_points_diff = -total_spent
