from typing import List, Dict
import json
import random
import traceback
import time

from chat_thief.log import logger
from chat_thief.audio_command import AudioCommand
from chat_thief.new_models.soundeffect_request import SoundeffectRequest
from chat_thief.chat_logs import ChatLogs
from chat_thief.user import User
from chat_thief.prize_dropper import drop_random_soundeffect_to_user
from chat_thief.irc import send_twitch_msg


def sync_main():
    while True:
        try:
            peasants = ChatLogs().recent_stream_peasants()
            result = drop_random_soundeffect_to_user(random.sample(peasants, 1)[0])
            send_twitch_msg(result)

            for peasant in peasants:
                user = User(peasant)
                if random.choice([0, 1]):
                    print(peasant)
                    user.add_street_cred()

            # Every 5 minutes, all the chatters have a chance at some street cred
            time.sleep(300)
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
