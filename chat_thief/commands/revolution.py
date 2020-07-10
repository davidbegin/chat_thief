from typing import List, Optional

import os
from itertools import chain, cycle

from chat_thief.models.user import User
from chat_thief.models.vote import Vote
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.models.command import Command
from chat_thief.models.breaking_news import BreakingNews


class Revolution:
    def __init__(self, revolutionary: str):
        self.revolutionary = revolutionary
        self.coup = Command("coup")

    def attempt_coup(self, tide: str) -> str:
        user = User(self.revolutionary)
        coup_cost = self.coup.cost()

        print(f"Cool Points: {user.cool_points()} | Coup Cost: {coup_cost}")

        if user.cool_points() >= coup_cost or self.revolutionary == "beginbotbot":
            print("WE HAVE ENOUGH FOR A REVOLUTION")
            user.update_cool_points(-coup_cost)
            self.coup.increase_cost(coup_cost * 2)

            if "TEST_MODE" not in os.environ:
                os.system(f"so {tide}")

            return self._turn_the_tides(tide)
        else:
            print(f"YOU CAN'T TRIGGER A REVOLUTION: {coup_cost}")
            self._punish_revolutionary()
            return f"@{self.revolutionary} is now Bankrupt, that will teach you a lesson. Coups require {coup_cost} Cool Points"

    # ================================================================

    def _punish_revolutionary(self) -> None:
        User(self.revolutionary).bankrupt()

    def _turn_the_tides(self, tide: str) -> str:
        fence_sitters = Vote.fence_sitters()
        user = User("beginbot")
        vote = Vote("beginbot")

        for fence_sitter in fence_sitters:
            fs = User(fence_sitter)
            # Maybe in peace time, you should only lose a fraction of your commands
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

        BreakingNews(
            user=self.revolutionary,
            scope=f"@{self.revolutionary} triggered a {tide} coup",
            category=tide,
            revolutionaries=revolutionaries,
            peace_keepers=peace_keepers,
            fence_sitters=fence_sitters,
        ).save()

        if tide == "peace":
            power_users = peace_keepers
            weaklings = revolutionaries
            self._transfer_power(peace_keepers, revolutionaries, revolutionary_sounds)
            return "REVOLUTIONS WILL NOT BE TOLERATED, AND REVOLUTIONARIES WILL BE PUNISHED"
        else:
            power_users = revolutionaries
            weaklings = peace_keepers

            # We need to remove all Revolution permissionns before
            for revolutionary in revolutionaries:
                User(revolutionary).remove_all_commands()

            self._transfer_power(
                revolutionaries,
                peace_keepers,
                peace_keeper_sounds + revolutionary_sounds,
            )
            return "THE REVOLUTION IS NOW!"

    #  Transferring power is Different
    def _transfer_power(
        self, power_users: List[str], weaklings: List[str], bounty: List[str]
    ) -> str:
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
