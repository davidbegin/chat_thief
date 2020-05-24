from typing import List, Dict
import json
import random
import traceback
import time
from datetime import datetime
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
    in_coup = False
    last_most_expensive = Command.most_expensive()
    last_cool_points = User.richest_cool_points()

    while True:
        os.system("clear")

        print(f"\nCommand: !{last_most_expensive['name']}")
        print(
            f"Cool Points: @{last_cool_points['name']} - {last_cool_points['cool_points']}"
        )

        # print(f"in coup: {in_coup}")

        try:
            new_top_cmd = Command.most_expensive()
            updated_cool_points = User.richest_cool_points()

            print(f"New Most Expensive: {new_top_cmd['name']}")
            print(f"Old Most Expensive: {last_most_expensive['name']}")

            if new_top_cmd["name"] != last_most_expensive["name"]:
                print(f"We have a new most expensive command: new_top_cmd['name']")
                last_most_expensive = new_top_cmd
                BreakingNews(
                    f"New Most Expensive Command: {new_top_cmd['name']} - 💸 {new_top_cmd['cost']}"
                ).save()

            elif updated_cool_points["name"] != last_cool_points["name"]:
                print(f"We have a new richest user: {updated_cool_points['name']}")
                last_cool_points = updated_cool_points
                BreakingNews(
                    scope=f"New Richest in Cool Points: {updated_cool_points['name']}",
                    user=updated_cool_points["name"],
                ).save()

            time.sleep(1)
        except Exception as e:
            time.sleep(30)

            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
