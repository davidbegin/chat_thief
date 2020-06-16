from chat_thief.new_commands.result import Result
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.models.user import User, PurchaseResult

class PurchaseReceipt:
    def __init__(self, user, sfx, result, cool_points, cost=None):
        self.user = user
        self.sfx = sfx
        self.cost = cost
        self.cool_points = cool_points
        self.result = result
        self.message = result.value.format(
            user=user, sfx=sfx, cost=cost, cool_points=cool_points
        )

    def __repr__(self):
        return f"PurchaseReceipt({self.user}, {self.sfx}, {self.result.name}, {self.cool_points}, {self.cost})"

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


        self.buy_sfx(user, target_sfx)

    def _buy_sfx(self, user, target_sfx):
        current_cool_points = user.cool_points()

        if effect not in SoundeffectsLibrary.fetch_soundeffect_names():
            return PurchaseReceipt(
                user=self.name,
                sfx=effect,
                result=PurchaseResult.InvalidSFX,
                cool_points=current_cool_points,
            )

        command = Command(effect)
        command_cost = command.cost()

        if Command(effect).allowed_to_play(self.name):
            return PurchaseReceipt(
                user=self.name,
                sfx=effect,
                cost=command_cost,
                result=PurchaseResult.AlreadyOwn,
                cool_points=current_cool_points,
            )

        if current_cool_points >= command_cost:
            self.update_cool_points(-command_cost)
            command.allow_user(self.name)
            command.increase_cost()

            return PurchaseReceipt(
                user=self.name,
                sfx=effect,
                cool_points=current_cool_points,
                result=PurchaseResult.SuccessfulPurchase,
                cost=command_cost,
            )
        else:
            return PurchaseReceipt(
                user=self.name,
                sfx=effect,
                cool_points=current_cool_points,
                result=PurchaseResult.TooPoor,
                cost=command_cost,
            )
