from chat_thief.models.user import User
from chat_thief.permissions_fetcher import PermissionsFetcher


class Revolution:
    def __init__(self, user_name):
        self.user_name = user_name
        self.user = User(self.user_name)
        self.cool_points = int(self.user.cool_points())

    def incite(self):
        if self.user_name == "beginbot" or self.cool_points > 99:
            self._revolution()
        elif self.user.total_cool_points() > 40:
            # Theres too many cool points
            return "COMING SOON A NEW JOINT REVOLUTION"
            # We want to remove all permissions and points
        else:
            return f"@{self.user_name} you need {99 - self.cool_points} more for a revolution"

    def _revolution(self):
        results = []
        result = self.user.purge()
        results.append(result)
        permissions_manager = PermissionsFetcher("beginbot")
        result = permissions_manager.purge()
        results.append(result)
        return results
