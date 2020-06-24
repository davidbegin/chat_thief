import traceback
import time
from datetime import datetime
import os

from chat_thief.chat_logs import ChatLogs
from chat_thief.config.log import logger
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.command import Command
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.models.user import User
from chat_thief.prize_dropper import drop_random_soundeffect_to_user


class BreakingNewsBot:
    def __init__(self):
        self.in_coup = False
        self.last_breaking_time = None
        self.initial_most_expensive = Command.most_expensive()
        self.initial_richest_user = User.richest_cool_points()

    def loop(self):

        while True:
            try:
                self.check_for_breaking_news()
                time.sleep(1)
            except Exception as e:
                time.sleep(30)
                # https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt
                # phaqui: KeyboardInterrupt does not inherit from Exception, so that
                # part of your code won't ever execute
                if e is KeyboardInterrupt:
                    raise e
                else:
                    traceback.print_exc()

    def check_for_breaking_news(self):
        if BreakingNews.unreported_news():
            last_news_story = BreakingNews.last()
            print(f"last news story: {last_news_story}")
            print(f"in coup: {self.in_coup}")
            print(f"Time since Last Breaking News: {self.last_breaking_time}")

            if self.last_breaking_time:
                how_long_since_break = datetime.now() - self.last_breaking_time
                print(f"How Long: {how_long_since_break}")

                # We Should also take into account the type of event
                # if how_long_since_break.seconds < 300:
                if how_long_since_break.seconds < 5:
                    # if how_long_since_break.seconds < 300:
                    print("Sorry Too Soon, waiting for more news")
                    time.sleep(3)
                else:
                    print("You have my permission to trigger breaking news")
                    self.trigger_breaking_news()
            else:
                print("Triggering Breaking News no previous news stories")
                self.trigger_breaking_news()

    def trigger_breaking_news(self):
        # The key here is that this, changes the news to be unreported
        news_story = BreakingNews.report_last_story()
        category = news_story.get("category", None)

        if category == "iasip":
            os.system("scene iasip")
            time.sleep(7)
            os.system("scene")
        elif category == "curb":
            os.system("scene curb")
        else:
            os.system("scene breakin")
            os.system("nomeme")
            time.sleep(7)
            os.system("nomeme")
            os.system("scene news")

        self.last_breaking_time = datetime.now()
        # os.system("time make deploy")


if __name__ == "__main__":
    BreakingNewsBot().loop()
