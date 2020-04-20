from chat_thief.user import User
from chat_thief.command_permissions import CommandPermissionCenter


class Revolution:
    def __init__(self, user_name):
        self.user_name = user_name
        self.user = User(self.user_name)
        self.cool_points = int(self.user.cool_points())

    def incite(self):
        if self.cool_points > 99 or self.user_name == "beginbotbot":
            results = []
            result = self.user.purge()
            results.append(result)
            permissions_manager = CommandPermissionCenter("beginbot")
            result = permissions_manager.purge()
            results.append(result)
            return results

            # We want to remove all permissions and points
        else:
            return f"@{self.user_name} you need {99 - self.cool_points} more for a revolution"
