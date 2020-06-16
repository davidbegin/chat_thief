from chat_thief.new_commands.result import Result
from chat_thief.models.user import User, PurchaseResult

# This sometimes Buys 1, othertimes many
# Should all Generic command class, be a single command
class Buyer:
    def __init__(self, user, target_sfx, amount=1):
        self._user = user
        self._target_sfx = target_sfx
        self._amount = amount

    def buy(self):
        results = []

        for _ in range(0, self._amount):
            result = self._try_and_buy()
            print(result)
            results.append(result)

        return Result(user=self._user, command="buy", results=results)

    def _try_and_buy(self):
        user = User(self._user)
        if self._target_sfx == "random":
            target_sfx = user._find_affordable_random_command().name
        else:
            target_sfx = self._target_sfx

        print(f"@{user} Attempting to buy {target_sfx}")
        return user.buy_sfx(target_sfx)
