from tinydb import Query
from chat_thief.database import db_table
from chat_thief.prize_dropper import drop_random_soundeffect_to_user
from chat_thief.irc import send_twitch_msg

db_path = "db/bets.json"
bets_db = db_table(db_path, "bets")

class CubeCasino():
    def __init__(self, user, args=[]):
        self.user = user
        self.args = args

    def closet_result(self, cube_time):
        bets = bets_db.all()
        result = {"bet": 1000000}
        for user_bet in bets:
            new_result = abs(user_bet['bet'] - cube_time)
            if new_result < result["bet"]:
                result = user_bet

        difference = abs(result['bet'] - cube_time)
        sfx_count = 10 - difference

        msg = f"Closest User is: @{result['better']}, and they've earned: {sfx_count} commands"

        if sfx_count > 0:
            for _ in range(0, sfx_count):
                send_twitch_msg(drop_random_soundeffect_to_user(result['better']))

        print(msg)
        return msg


    def bet(self):
        self.user_bet = int(self.args[0])
        if self.user_bet < 1:
            raise ValueError("Cmon Beginbot can't solve a Cube in negative time....yet")

        bets_db.insert(self.doc())
        return self.doc()

    def purge(self):
        return bets_db.purge()

    def doc(self):
        return {
                "better": self.user,
                "bet": self.user_bet
                }
