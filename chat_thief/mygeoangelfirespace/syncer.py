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
from chat_thief.models.user import User
from chat_thief.prize_dropper import drop_random_soundeffect_to_user


# I feel like this could also handle checking for the news
def sync_main():
    while True:
        try:
            # os.system("time make full_deploy")
            os.system("time make deploy")
            time.sleep(300)
            # time.sleep(60)
        except Exception as e:
            time.sleep(30)
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
