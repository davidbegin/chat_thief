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
    os.system("clear")

    last_most_expensive = Command.most_expensive()
    last_richest_street_cred = User.richest_street_cred()
    last_richest_cool_points = User.richest_cool_points()

    while True:
        print()
        # We should only print them if they are different
        print(f"Most Expensive Command: !{last_most_expensive['name']}")
        print(
            f"Most Street Cred      : @{last_richest_street_cred['name']} - {last_richest_street_cred['street_cred']}"
        )
        print(
            f"Most Cool Points      : @{last_richest_cool_points['name']} - {last_richest_cool_points['cool_points']}"
        )

        new_most_street_cred = User.richest_street_cred()
        new_most_cool_points = User.richest_cool_points()

        try:
            # How do we know it's a revolution???

            if Command.most_expensive()["name"] != last_most_expensive["name"]:
                last_most_expensive = Command.most_expensive()
                BreakingNews(
                    f"New Most Expensive Command: {last_most_expensive}"
                ).save()
                os.system("scene breakin")

            elif new_most_street_cred["name"] != last_richest_street_cred["name"]:
                last_richest_street_cred = new_most_street_cred

                BreakingNews(
                    scope=f"New Richest in Street User: {new_most_street_cred['name']}",
                    user=new_most_street_cred["name"],
                ).save()

                os.system("scene breakin")

            elif new_most_cool_points["name"] != last_richest_cool_points["name"]:
                last_richest_cool_points = new_most_cool_points

                BreakingNews(
                    scope=f"New Richest in Cool Points: {new_most_cool_points['name']}",
                    user=new_most_cool_points["name"],
                ).save()

                os.system("scene breakin")

            time.sleep(30)
            # time.sleep(300)
        except Exception as e:
            time.sleep(30)
            # https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt
            # phaqui: KeyboardInterrupt does not inherit from Exception, so that
            # part of your code won't ever execute
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
