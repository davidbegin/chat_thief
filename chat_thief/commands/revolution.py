from itertools import chain, cycle

from chat_thief.models.user import User
from chat_thief.models.vote import Vote
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.models.command import Command


# 2 Paths for Coup:
#   - Peace
#       - Voted For Peace:
#           - Get a cut of the revolutionaries, sounds and points
#       - Voted for Revolution:
#           -  You lose it all
#   - Revolution
#       - Voted For Peace:
#           -  You lose it all
#       - Voted for Revolution:
#           - You will get a small selections of founds


class Revolution:
    # Where should I pass in the user?
    def __init__(self, revolutionary):
        self.revolutionary = revolutionary
        self.coup = Command("coup")

    def attempt_coup(self, tide):
        user = User(self.revolutionary)

        if user.cool_points() >= self.coup.cost():
            print("WE HAVE ENOUGH FOR A REVOLUTION")
            # user.remove_cool_points(self.coup.cost())
            # self.coup.increase_cost(self.coup.cost() * 2)
            # self._turn_the_tides(tide)
        else:
            print("YOU CAN'T TRIGGER A REVOLUTION")
            # return self._punish_revolutionary()

    def _punish_revolutionary(self):
        return User(self.revolutionary).bankrupt()

    def _turn_the_tides(self, tide):
        user = User("beginbot")
        vote = Vote("beginbot")

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
            return self._transfer_power(
                peace_keepers, revolutionaries, revolutionary_sounds
            )

        if tide == "revolution":
            return self._transfer_power(
                revolutionaries, peace_keepers, peace_keeper_sounds
            )

    #  Transferring power is Different
    def _transfer_power(self, power_users, weaklings, bounty):
        the_cycle_of_power_users = cycle(power_users)

        for user in weaklings:
            print(f"Removing All Commands for {user}")
            User(user).remove_all_commands()

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
