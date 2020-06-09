import datetime

from chat_thief.routers.base_router import BaseRouter
from chat_thief.models.cube_bet import CubeBet
from chat_thief.models.cube_stats import CubeStats
from chat_thief.commands.cube_casino import CubeCasino
from chat_thief.chat_parsers.command_parser import CommandParser


class CubeCasinoRouter(BaseRouter):
    def route(self):
        if self.command in ["all_bets", "all_bet", "bets"]:
            return " | ".join([f"@{bet[0]}: {bet[1]}" for bet in CubeBet.all_bets()])

        if self.command == "bet":
            if not CubeCasino.is_stopwatch_running():
                parser = CommandParser(
                    user=self.user, command=self.command, args=self.args
                ).parse()
                result = CubeBet(name=self.user, duration=parser.amount).save()
                return (
                    f"Thank you for your bet: @{result['name']}: {result['duration']}s"
                )
            else:
                return f"NO BETS WHILE BEGINBOT IS SOLVING"

        if self.command == "cubed" and self.user in ["beginbot", "beginbotbot"]:
            cube_time = self._convert_cube_time()
            result = CubeCasino(cube_time).gamble()
            CubeBet.purge()
            return result

        if self.command == "new_cube" and self.user == "beginbotbot":
            return CubeBet.purge()

    def _convert_cube_time(self):
        try:
            return int(self.args[0])
        except:
            hours, minutes, seconds = self.args[0].split(":")
            return datetime.timedelta(
                hours=int(hours), minutes=int(minutes), seconds=int(seconds)
            ).seconds
