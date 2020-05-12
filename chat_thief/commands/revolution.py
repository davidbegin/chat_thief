from itertools import chain, cycle

from chat_thief.models.user import User
from chat_thief.models.vote import Vote
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.models.command import Command


class Revolution:
    def __init__(self, revolutionary):
        self.revolutionary = revolutionary
        self.coup = Command("coup")

    def attempt_coup(self, tide):
        user = User(self.revolutionary)

        print(f"Cool Points: {user.cool_points()} | Coup Cost: {self.coup.cost()}")

        if user.cool_points() >= self.coup.cost():
            print("WE HAVE ENOUGH FOR A REVOLUTION")
            user.update_cool_points(-self.coup.cost())
            self.coup.increase_cost(self.coup.cost() * 2)
            return self._turn_the_tides(tide)
        else:
            print(f"YOU CAN'T TRIGGER A REVOLUTION: self.coup.cost()")
            return self._punish_revolutionary()

    def _punish_revolutionary(self):
        return User(self.revolutionary).bankrupt()

    def _turn_the_tides(self, tide):
        fence_sitters = Vote.fence_sitters()
        user = User("beginbot")
        vote = Vote("beginbot")

        for fence_sitter in fence_sitters:
            fs = User(fence_sitter)
            fs.remove_all_commands()
            if tide == "revolution":
                print(fs.bankrupt())

        revolutionaries = vote.revolutionaries()
        peace_keepers = vote.peace_keepers()

        revolutionary_sounds = list(
            chain.from_iterable([User(user).commands() for user in revolutionaries])
        )

        peace_keeper_sounds = list(
            chain.from_iterable([User(user).commands() for user in peace_keepers])
        )

        print(f"Revolutionaries: {revolutionaries}")
        print(f"Sounds: {revolutionary_sounds}\n")
        print(f"Peace Keepers: {peace_keepers}")
        print(f"Sounds: {peace_keeper_sounds}\n")

        if tide == "peace":
            power_users = peace_keepers
            weaklings = revolutionaries
            self._transfer_power(peace_keepers, revolutionaries, revolutionary_sounds)
            return [
                f"Power Users: { ' '.join(power_users)}",
                f"Weaklings: { ' '.join(weaklings)}",
                f"Fence Sitters: { ' '.join(fence_sitters)}",
            ]

        if tide == "revolution":
            power_users = revolutionaries
            weaklings = peace_keepers

            # We need to remove all Revolution permissionns before
            for revolutionary in revolutionaries:
                print(User(revolutionary).remove_all_commands())

            self._transfer_power(
                revolutionaries,
                peace_keepers,
                peace_keeper_sounds + revolutionary_sounds,
            )
            return [
                f"Power Users: { ' '.join(power_users)}",
                f"Weaklings: { ' '.join(weaklings)}",
                f"Fence Sitters: { ' '.join(fence_sitters)}",
            ]

    #  Transferring power is Different
    def _transfer_power(self, power_users, weaklings, bounty):
        the_cycle_of_power_users = cycle(power_users)

        for user in weaklings:
            print(f"Removing All Commands for {user}")
            poor_sap = User(user)
            poor_sap.remove_all_commands()
            poor_sap.bankrupt()

        for sfx in bounty:
            user = next(the_cycle_of_power_users)
            print(f"Giving {user} SFX: {sfx}")
            Command(sfx).allow_user(user)

        return f"Power Transferred: {power_users} | {weaklings} | {bounty}"

    # It should cost to coup
    def _revolution(self):
        results = []
        result = self.user.purge()
        results.append(result)
        permissions_manager = PermissionsFetcher("beginbot")
        result = permissions_manager.purge()
        results.append(result)
        return results
