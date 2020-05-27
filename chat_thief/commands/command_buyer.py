from chat_thief.models.user import User, PurchaseResult


class CommandBuyer:
    def __init__(self, user, target_sfx, amount=1):
        self.amount = amount
        self.user = User(user)
        self.target_sfx = target_sfx

    def new_buy(self):
        results = []

        for _ in range(0, self.amount):
            result = self._try_and_buy()
            print(result)
            results.append(result)

        return self._format_results(results)

    def _format_results(self, results):
        total_spent = sum([result.cost for result in results])
        sfx_names = " ".join(["!" + result.sfx for result in results])

        successful_purchase = all(
            [result.result == PurchaseResult.SuccessfulPurchase for result in results]
        )
        if successful_purchase:
            return f"@{self.user.name} bought {len(results)} SFXs: {sfx_names} for a Total of {total_spent}"
        else:
            if len(results) == 1:
                return results[0].message
            else:
                return [result.message for result in results]

    def _try_and_buy(self):
        if self.target_sfx == "random":
            target_sfx = self.user._find_affordable_random_command().name
        else:
            target_sfx = self.target_sfx

        print(f"@{self.user.name} Attempting to buy {target_sfx}")
        return self.user.buy_sfx(target_sfx)
