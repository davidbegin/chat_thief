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
from chat_thief.models.command import Command
from chat_thief.prize_dropper import drop_random_soundeffect_to_user

BLACKLIST = []


def sync_main():
    last_most_expensive = Command.most_expensive()

    while True:
        try:
            if Command.most_expensive() != last_most_expensive:
                last_most_expensive = Command.most_expensive()
                BreakingNews(f"New Most Expensive Command: {last_most_expensive}").save()
                os.system("scene breakin")

            # send_twitch_msg(result)

            time.sleep(30)
        except Exception as e:
            # https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt
            time.sleep(30)
            # phaqui: KeyboardInterrupt does not inherit from Exception, so that part of your code won't ever execute
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
