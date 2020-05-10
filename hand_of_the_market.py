from typing import List, Dict
import json
import random
import traceback
import time

from chat_thief.config.log import logger
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.chat_logs import ChatLogs
from chat_thief.models.user import User
from chat_thief.prize_dropper import drop_random_soundeffect_to_user
from chat_thief.irc import send_twitch_msg

BLACKLIST = []


def sync_main():
    while True:
        try:
            peasants = ChatLogs().recent_stream_peasants()
            result = drop_random_soundeffect_to_user(random.sample(peasants, 1)[0])
            send_twitch_msg(result)

            for peasant in peasants:
                if peasant not in BLACKLIST:
                    user = User(peasant)
                    user_karma = user.karma()
                    print(f"@{peasant} Karma: {user.karma()}")
                    user.update_street_cred(1 + user_karma)
                    user.revive()

            formatted_peasants = [f"@{peasant}" for peasant in peasants]
            send_twitch_msg(
                f"Squid1 Enjoy your street cred: {' '.join(formatted_peasants)} Squid4"
            )

            # Every 10 minutes, all the chatters have a chance at some street cred
            time.sleep(600)
        except Exception as e:
            time.sleep(30)
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
