from typing import List, Dict
import json
import random
import traceback
import time
from datetime import datetime
import os

from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.user import User
from chat_thief.models.command import Command


HOW_MANY_SECONDS_BETWEEN_NEWS = 300


class ForbesBot:
    def __init__(self):
        self.last_breaking_time = None
        self.last_most_expensive = Command.most_expensive()
        self.last_cool_points = User.richest_cool_points()

    def loop(self):
        while True:
            os.system("clear")

            print(f"\nCommand: !{self.last_most_expensive['name']}")
            print(
                f"Cool Points: @{self.last_cool_points['name']} - {self.last_cool_points['cool_points']}"
            )

            if self.last_breaking_time:
                how_long_since_break = datetime.now() - self.last_breaking_time
                print(
                    f"How Long: {how_long_since_break} / {HOW_MANY_SECONDS_BETWEEN_NEWS}"
                )

            try:
                self.new_top_cmd = Command.most_expensive()
                self.updated_cool_points = User.richest_cool_points()

                print(f"New Most Expensive: {self.new_top_cmd['name']}")
                print(f"Old Most Expensive: {self.last_most_expensive['name']}")

                if self.new_top_cmd["name"] != self.last_most_expensive["name"]:
                    print(
                        f"We have a new most expensive command: self.new_top_cmd['name']"
                    )
                    self.last_most_expensive = self.new_top_cmd

                    if self.last_breaking_time:
                        how_long_since_break = datetime.now() - self.last_breaking_time
                        print(f"How Long: {how_long_since_break}")

                        if how_long_since_break.seconds > HOW_MANY_SECONDS_BETWEEN_NEWS:
                            self.breaking_news(
                                f"New Most Expensive Command: {self.new_top_cmd['name']} - 💸{ self.new_top_cmd['cost']}"
                            ).save()
                    else:
                        self.breaking_news(
                            msg=f"New Most Expensive Command: {self.new_top_cmd['name']} - 💸{ self.new_top_cmd['cost']}"
                        )

                elif self.updated_cool_points["name"] != self.last_cool_points["name"]:
                    print(
                        f"We have a new richest user: {self.updated_cool_points['name']}"
                    )
                    self.last_cool_points = self.updated_cool_points
                    if self.last_breaking_time:
                        how_long_since_break = datetime.now() - self.last_breaking_time
                        print(f"How Long: {how_long_since_break}")

                        if how_long_since_break.seconds > 300:
                            self.breaking_news(
                                msg=f"New Richest in Cool Points: {self.updated_cool_points['name']}",
                                user=self.updated_cool_points["name"],
                            )
                    else:
                        self.breaking_news(
                            msg=f"New Richest in Cool Points: {self.updated_cool_points['name']}",
                            user=self.updated_cool_points["name"],
                        )

                time.sleep(1)
            except Exception as e:
                traceback.print_exc()
                time.sleep(1)

                if e is KeyboardInterrupt:
                    raise e

    def breaking_news(self, msg, user=None):
        self.last_breaking_time = datetime.now()
        BreakingNews(scope=msg, user=user,).save()


if __name__ == "__main__":
    ForbesBot().loop()
