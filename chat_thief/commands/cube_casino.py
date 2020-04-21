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

    def all_bets(self):
        return " | ".join([
            f"@{result['gambler']} - {result['bet']}" for result in bets_db.all()
        ])

    def closet_result(self, cube_time):
        result = {"gambler": None, "bet": 1000000}

        for user_bet in bets_db.all():
            bet_diff = abs(user_bet['bet'] - cube_time)
            print(f"{user_bet['gambler']} Diff: {bet_diff}")

            if bet_diff < abs(result["bet"] - cube_time):
                result = user_bet

        sfx_count = 10 - abs(result['bet'] - cube_time)
        msg = f"Closest User is: @{result['gambler']}, and they've earned: {sfx_count} commands"

        for _ in range(0, sfx_count):
            send_twitch_msg(drop_random_soundeffect_to_user(result['gambler']))

        print(msg)
        return msg


    def bet(self):
        self.user_bet = int(self.args[0])
        if self.user_bet < 1:
            raise ValueError("Cmon Beginbot can't solve a Cube in negative time....yet")

        old_bets = bets_db.search(
            Query().gambler == self.user
        )

        if old_bets:
            return f"@{self.user} you already bet!"
        else:
            bets_db.insert(self.doc())
            return self.doc()

    def purge(self):
        bets_db.purge()
        return "Purged the Bets DB"

    def doc(self):
        return {
            "gambler": self.user,
            "bet": self.user_bet
        }
