import subprocess
from itertools import cycle
import os
import random

from tinydb import Query

from chat_thief.models.cube_bet import CubeBet
from chat_thief.models.cube_stats import CubeStats
from chat_thief.models.user import User
from chat_thief.models.database import db_table
from chat_thief.commands.command_giver import CommandGiver
from chat_thief.prize_dropper import drop_random_soundeffect_to_user
from chat_thief.irc import send_twitch_msg


class CubeCasino:
    def __init__(self, solve_time):
        self._solve_time = solve_time

        if CubeCasino.is_stopwatch_running():
            raise Exception("YOU CAN'T BET WHILE THE BEGIN IS SOLVING")

    def gamble(self):
        winning_duration, winners, losers, all_bets = self._winners()

        CubeStats(
            winning_duration=winning_duration, winners=winners, all_bets=all_bets
        ).save()

        return self._winner_winner_chicken_dinnner(
            winners, winning_duration, cycle(losers)
        )

    def _winners(self):
        all_bets = CubeBet.all_bets()

        if all_bets == []:
            return (None, None, [])

        exact_winners = [bet[0] for bet in all_bets if bet[1] == self._solve_time]

        winning_duration = 1000
        if exact_winners:
            losers = list(set([bet[0] for bet in all_bets]) - set(exact_winners))
            return (self._solve_time, exact_winners, losers, all_bets)

        for user, guess in all_bets:
            bet_diff = guess - self._solve_time
            print(f"@{user} Bet Diff: {bet_diff}")

            current_diff = winning_duration - self._solve_time
            if abs(bet_diff) < abs(current_diff):
                winning_duration = guess

        winners = [bet[0] for bet in all_bets if bet[1] == winning_duration]
        losers = list(set([bet[0] for bet in all_bets]) - set(winners))

        return (
            winning_duration,
            winners,
            losers,
            all_bets,
        )

    def _winner_winner_chicken_dinnner(self, winners, winning_duration, losers):
        sfx_count = 10 - abs(winning_duration - self._solve_time)
        sfx_per_user = round(sfx_count / len(winners))
        msg = []

        for winner in winners:
            msg.append(f"Winner: @{winner} Won {sfx_per_user} commands")

            for _ in range(0, sfx_per_user):
                loser, command = self._find_command(losers)

                if command:
                    msg = CommandGiver(
                        user=winner, command=command, friend=loser,
                    ).give()
                    send_twitch_msg(msg)
        return msg

    def _find_command(self, losers):
        loser = next(losers)
        commands = User(loser).commands()

        if commands:
            command = random.sample(commands, 1)
            return loser, command
        else:
            return loser, None

    @staticmethod
    def is_stopwatch_running():
        if "TEST_MODE" in os.environ:
            return False

        args = "ps -ef".split(" ")
        processes = subprocess.run(args, capture_output=True).stdout
        result = "bash ./stopwatch" in str(processes)
        print(f"Stop Watch Running: {result}")
        return result
