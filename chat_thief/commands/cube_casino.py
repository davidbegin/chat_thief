import subprocess
from itertools import cycle
import os
import random

from tinydb import Query

from chat_thief.models.cube_bet import CubeBet
from chat_thief.models.cube_stats import CubeStats
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.models.database import db_table
from chat_thief.commands.command_giver import CommandGiver
from chat_thief.prize_dropper import drop_random_soundeffect_to_user
from chat_thief.irc import send_twitch_msg
from chat_thief.begin_fund import BeginFund, random_soundeffect


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

        results = []
        try:
            loser_commands = self._winner_winner_chicken_dinnner(
                winners, winning_duration, iter(losers)
            )
            losers_diff = list(
                set(losers) - set([loser for loser, command in loser_commands])
            )
            winners_circle = cycle(winners)
            for (loser, command) in loser_commands:
                winner = next(winners_circle)
                result = CommandGiver(user=loser, command=command, friend=winner).give()
                results += result

            for loser in losers_diff:
                loser_commands = User(loser).commands()
                if loser_commands:
                    result = Command(loser_commands[0]).unallow_user(loser)
                    results.append(result)
                else:
                    target_sfx = random_soundeffect()
                    return BeginFund(
                        target_user=winner, target_command=target_sfx
                    ).drop()

            send_twitch_msg(results)
            return results
        except Exception as e:
            print(e)
            send_twitch_msg(f"Error Rewarding Winner: {e}")
            send_twitch_msg(results)
            return

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

            # We need to find the commands
            # that we are giving to the winner
            # Find all the losers, who we are just removing a command

            spoils_of_war = []
            for _ in range(0, sfx_per_user):
                looking_for_loser = True

                while looking_for_loser:
                    command = None
                    loser = next(losers)
                    commands = User(loser).commands()

                    if commands:
                        command = random.sample(commands, 1)[0]

                    if command:
                        looking_for_loser = False
                        spoils_of_war.append((loser, command))

                        # msg = CommandGiver(
                        #     user=loser, command=command, friend=winner,
                        # ).give()

                        # send_twitch_msg(msg)
        # return msg
        return spoils_of_war

    @staticmethod
    def is_stopwatch_running():
        if "TEST_MODE" in os.environ:
            return False

        args = "ps -ef".split(" ")
        processes = subprocess.run(args, capture_output=True).stdout
        result = "bash ./stopwatch" in str(processes)
        print(f"Stop Watch Running: {result}")
        return result
