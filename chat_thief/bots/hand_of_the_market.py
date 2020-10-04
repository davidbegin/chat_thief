from typing import List, Dict
import json
import random
import traceback
import time
import os

from chat_thief.chat_logs import ChatLogs
from chat_thief.config.log import logger
from chat_thief.irc import send_twitch_msg
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.user import User
from chat_thief.prize_dropper import drop_random_soundeffect_to_user


# I feel like this could also handle checking for the news
def sync_main():
    PlaySoundeffectRequest(user="beginbotbot", command="openingbell").save()

    while True:
        try:
            peasants = ChatLogs().recent_stream_peasants()
            print(f"\n\npeasants {peasants}\n\n")

            # We need to make this better
            result = drop_random_soundeffect_to_user(random.sample(peasants, 1)[0])
            send_twitch_msg(result)

            for peasant in peasants:
                user = User(peasant)
                user_karma = user.karma()
                print(f"@{peasant} Karma: {user.karma()}")
                user.update_street_cred(1)
                # user.update_street_cred(1 + user_karma)
                user.revive(3 + user_karma)

            # Should I tell people this when mana dropped.
            send_twitch_msg("CoolCat CoolCat CoolCat")

            # formatted_peasants = [f"@{peasant}" for peasant in peasants]
            # send_twitch_msg(
            #     f"Squid1 Enjoy your street cred: {' '.join(formatted_peasants)} Squid4"
            # )

            # Every 5 minutes, all the chatters have a chance at some street cred
            # os.system("time make deploy")
            time.sleep(300)
        except Exception as e:
            time.sleep(30)
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
