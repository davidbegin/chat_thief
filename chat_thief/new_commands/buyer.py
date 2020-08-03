from typing import Optional

from chat_thief.new_commands.result import Result
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary
from chat_thief.models.user import User
from chat_thief.models.command import Command

from enum import Enum


class PurchaseResult(Enum):
    AlreadyOwn = "@{user} already has access to !{sfx}"
    InvalidSFX = "Invalid Effect: {sfx}"
    TooPoor = "@{user} not enough Cool Points to buy !{sfx} - {cool_points}/{cost}"
    SuccessfulPurchase = "@{user} bought !{sfx} for {cost} Cool Points"


class PurchaseReceipt:
    def __init__(
        self,
        user: str,
        sfx: str,
        result: PurchaseResult,
        cool_points: int,
        cost: Optional[int] = None,
    ):
        self.user = user
        self.sfx = sfx
        self.cost = cost
        self.cool_points = cool_points
        self.result = result
        self.message = result.value.format(
            user=user, sfx=sfx, cost=cost, cool_points=cool_points
        )

    def __repr__(self) -> str:
        return f"PurchaseReceipt({self.user}, {self.sfx}, {self.result.name}, {self.cool_points}, {self.cost})"


# This sometimes Buys 1, othertimes many
# Should all Generic command class, be a single command
# Need a unifed return type for all
class Buyer:
    def __init__(self, user: str, target_sfx: str, amount: int = 1):
        self._user = user
        self._target_sfx = target_sfx
        self._amount = amount

    def buy(self) -> Result:
        results = []

        # Trying to buy a lot of one thing
        # this is for repeated random buys
        if self._amount > 1 and self._target_sfx != "random":
            raise ValueError(f"Stop Spamming: {self._user}")

        for _ in range(0, self._amount):
            result = self._try_and_buy()
            print(result)
            results.append(result)

        metadata = {"purchase_results": results}

        return Result(user=self._user, command="buy", metadata=metadata)

    def _try_and_buy(self) -> PurchaseReceipt:
        user = User(self._user)

        if self._target_sfx == "random":
            target_sfx = user._find_affordable_random_command().name
        else:
            target_sfx = self._target_sfx

        print(f"@{user} Attempting to buy {target_sfx}")

        return self._buy_sfx(user, target_sfx)

    def _buy_sfx(self, user: User, effect: str) -> PurchaseReceipt:
        current_cool_points = user.cool_points()

        if effect not in SoundeffectsLibrary.fetch_soundeffect_names():
            return PurchaseReceipt(
                user=user.name,
                sfx=effect,
                result=PurchaseResult.InvalidSFX,
                cool_points=current_cool_points,
            )

        command = Command(effect)
        command_cost = command.cost()

        if Command(effect).allowed_to_play(user.name):
            return PurchaseReceipt(
                user=user.name,
                sfx=effect,
                cost=command_cost,
                result=PurchaseResult.AlreadyOwn,
                cool_points=current_cool_points,
            )

        if current_cool_points >= command_cost:
            user.update_cool_points(-command_cost)
            command.allow_user(user.name)
            command.increase_cost()

            return PurchaseReceipt(
                user=user.name,
                sfx=effect,
                cool_points=current_cool_points,
                result=PurchaseResult.SuccessfulPurchase,
                cost=command_cost,
            )
        else:
            return PurchaseReceipt(
                user=user.name,
                sfx=effect,
                cool_points=current_cool_points,
                result=PurchaseResult.TooPoor,
                cost=command_cost,
            )
