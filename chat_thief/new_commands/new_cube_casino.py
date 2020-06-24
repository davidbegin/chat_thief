import os
import random
import subprocess

from chat_thief.models.cube_bet import CubeBet
from chat_thief.models.command import Command
from chat_thief.commands.command_giver import CommandGiver


class NewCubeCasino:
    def __init__(self, solve_time):
        self._solve_time = solve_time

        if NewCubeCasino.is_stopwatch_running():
            raise Exception("YOU CAN'T BET WHILE THE BEGIN IS SOLVING")

    def gamble(self):
        transfer_of_wealth = self._match_winners_and_losers()

        for winner, loser, command in transfer_of_wealth:
            print(f"@{winner} won !{command} from @{loser}")
            result = CommandGiver(user=loser, command=command, friend=winner).give()

        return transfer_of_wealth

    def _match_winners_and_losers(self):
        all_bets = CubeBet.all_bets()
        winners, loser_commands, winning_bet = self._find_winners_and_losers(all_bets)

        transfer_of_wealth = []

        # We have to sort winners by their bet amount
        for winner in winners:
            user, bet, wager = winner
            bet_amount = sum([Command(command).cost() for command in wager])
            commands_to_win = [
                loser for loser in loser_commands if loser[2] <= bet_amount
            ]

            while bet_amount > 0 and len(commands_to_win) > 0:
                random.shuffle(commands_to_win)
                command_tuple = commands_to_win.pop()

                # We remove the Command, so others Winners can't win it
                loser_commands.remove(command_tuple)
                loser, command, cost = command_tuple
                bet_amount -= cost
                transfer_obj = (user, loser, command)
                print(f"Transfer Obj: {transfer_obj}")
                transfer_of_wealth.append(transfer_obj)

        return transfer_of_wealth

    def _find_winners_and_losers(self, all_bets):
        winning_duration = 1000
        exact_winners = [bet for bet in all_bets if bet[1] == self._solve_time]
        winner_names = [winner[0] for winner in exact_winners]

        if exact_winners:
            print(f"\nExact Winners: {winner_names}\n")
            losers = [bet for bet in all_bets if bet[0] not in winner_names]
            winners = exact_winners
            winning_duration = self._solve_time
        else:
            for user, guess, _ in all_bets:
                bet_diff = guess - self._solve_time
                print(f"@{user} Bet Diff: {bet_diff}")

                current_diff = winning_duration - self._solve_time
                if abs(bet_diff) < abs(current_diff):
                    winning_duration = guess

            winners = [bet for bet in all_bets if bet[1] == winning_duration]
            winner_names = [winner[0] for winner in winners]
            print(f"\nCloset Winners: {winner_names}\n")
            losers = [bet for bet in all_bets if bet[0] not in winner_names]

        loser_names = [loser[0] for loser in losers]
        loser_commands = []

        print(f"Winners: {winner_names}\n")
        print(f"Losers: {loser_names}\n")

        for loser in losers:
            user, bet, wager = loser
            for command in wager:
                # if loser[0] != winner[0]:
                loser_command = (user, command, Command(command).cost())
                loser_commands.append(loser_command)

        return winners, loser_commands, winning_duration

    @staticmethod
    def is_stopwatch_running():
        if "TEST_MODE" in os.environ:
            return False

        args = "ps -ef".split(" ")
        processes = subprocess.run(args, capture_output=True).stdout
        result = "bash ./stopwatch" in str(processes)
        print(f"Stop Watch Running: {result}")
        return result
