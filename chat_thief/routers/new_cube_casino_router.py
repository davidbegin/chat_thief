import datetime

from chat_thief.routers.base_router import BaseRouter
from chat_thief.models.cube_bet import CubeBet
from chat_thief.models.user import User
from chat_thief.new_commands.new_cube_casino import NewCubeCasino
from chat_thief.chat_parsers.cube_casino_parser import CubeCasinoParser
from chat_thief.formatters.cube_casino_formatter import CubeCasinoFormatter


class NewCubeCasinoRouter(BaseRouter):
    def route(self):
        if self.command == "bet":
            return self._process_bet()

        elif self.command == "cubed" and self.user == "beginbotbot":
            return self._process_solve()

        elif self.command in ["all_bets", "all_bet", "bets"]:
            return " | ".join([f"@{bet[0]}: {bet[1]}" for bet in CubeBet.all_bets()])

        elif self.command == "new_cube" and self.user == "beginbotbot":
            return CubeBet.purge()

    def _process_solve(self):
        cube_time = self._convert_cube_time()
        result = NewCubeCasino(cube_time).gamble()
        CubeBet.truncate()
        result = CubeCasinoFormatter(result).format()
        print(f"Result from formatter: {result}")
        return result

    def _process_bet(self):
        parser = CubeCasinoParser(
            user=self.user, command=self.command, args=self.args
        ).parse()

        if NewCubeCasino.is_stopwatch_running():
            return f"NO BETS WHILE BEGINBOT IS SOLVING"

        wager = parser.wager
        if wager == []:
            wager = User(self.user).commands()

        if wager:
            result = CubeBet(
                user=self.user, duration=parser.bet, wager=wager
            ).create_or_update()
            return f"@{self.user} Thank you for your bet: {parser.bet}s - {len(wager)} Commands"
        else:
            return f"@{self.user} you must own at least 1 soundeffect to bet!"

    def _convert_cube_time(self):
        try:
            return int(self.args[0])
        except:
            hours, minutes, seconds = self.args[0].split(":")
            return datetime.timedelta(
                hours=int(hours), minutes=int(minutes), seconds=int(seconds)
            ).seconds
