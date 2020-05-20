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


class BreakingNewsBot:
    def __init__(self):
        self.in_coup = False
        self.last_breaking_time = None
        self.initial_most_expensive = Command.most_expensive()
        self.initial_richest_user = User.richest_cool_points()

    def loop(self):
        os.system("clear")

        while True:
            try:
                self.check_for_breaking_news()
                time.sleep(3)
            except Exception as e:
                time.sleep(30)
                # https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt
                # phaqui: KeyboardInterrupt does not inherit from Exception, so that
                # part of your code won't ever execute
                if e is KeyboardInterrupt:
                    raise e
                else:
                    traceback.print_exc()

    # Return Breaking News if exists
    def check_for_breaking_news(self):
        if BreakingNews.unreported_news():
            last_news_story = BreakingNews.last()
            print(f"last news story: {last_news_story}")
            print(f"in coup: {self.in_coup}")
            print(f"Time since Last Breaking News: {self.last_breaking_time}")

            if self.last_breaking_time:
                how_long_since_break = datetime.now() - self.last_breaking_time
                print(f"How Long: {how_long_since_break}")
                if how_long_since_break.seconds < 30:
                # if how_long_since_break.seconds < 300:
                    print("Sorry Too Soon, waiting for more news")
                    time.sleep(3)
                else:
                    print("You have my permission to trigger breaking news")
                    self.trigger_breaking_news()
            else:
                print("Triggering Breaking News no previous news stories ")
                self.trigger_breaking_news()

    def trigger_breaking_news(self):
        # Let's mark the news as reported on
        news_story = BreakingNews.report_last_story()

        os.system("scene breakin")
        os.system("nomeme")
        time.sleep(7)
        os.system("nomeme")
        os.system("scene news")
        self.last_breaking_time = datetime.now()


        # os.system("clear")

        # while True:
        #     print(f"\nMost Expensive Command: !{last_most_expensive['name']}")
        #     print(
        #         f"Most Street Cred      : @{last_richest_street_cred['name']} - {last_richest_street_cred['street_cred']}"
        #     )
        #     print(
        #         f"Most Cool Points      : @{last_richest_cool_points['name']} - {last_richest_cool_points['cool_points']}"
        #     )

        #     new_most_street_cred = User.richest_street_cred()
        #     new_most_cool_points = User.richest_cool_points()
        #     new_most_expensive_command = Command.most_expensive()
        #     last_news_story = BreakingNews.last()
        #     print(f"last news story: {last_news_story}")
        #     print(f"in coup: {in_coup}")
        #     # print(f"Time since Last Breaking News: {last_breaking_time}")

        #     if last_breaking_time:
        #         how_long_since_break = datetime.now() - last_breaking_time
        #         print(f"How Long: {how_long_since_break}")
        #         if how_long_since_break.seconds < 300:
        #             print("Sorry Too Soon, waiting for more news")
        #             time.sleep(3)
        #             continue
        #         else:
        #             print("You have my permission to trigger breaking news")

        #     try:
        #         if not last_news_story:
        #             in_coup = False

        #         print(f"New Most Expensive: {new_most_expensive_command['name']}")
        #         print(f"Old Most Expensive: {last_most_expensive['name']}")

        #         if last_news_story:
        #             last_category = last_news_story.get("category", None)
        #             print(f"Category of Most Recent News Story: {last_category}")

        #             if last_category in ["peace", "revolution"] and not in_coup:
        #                 in_coup = True
        #                 last_breaking_time = datetime.now()
        #                 trigger_breaking_news()
        #                 time.sleep(3)
        #                 continue

        #         if new_most_expensive_command["name"] != last_most_expensive["name"]:
        #             last_most_expensive = new_most_expensive_command
        #             BreakingNews(
        #                 f"New Most Expensive Command: {new_most_expensive_command['name']} - 💸 {new_most_expensive_command['cost']}"
        #             ).save()
        #             last_breaking_time = datetime.now()
        #             trigger_breaking_news()

        #         elif new_most_cool_points["name"] != last_richest_cool_points["name"]:
        #             last_richest_cool_points = new_most_cool_points
        #             BreakingNews(
        #                 scope=f"New Richest in Cool Points: {new_most_cool_points['name']}",
        #                 user=new_most_cool_points["name"],
        #             ).save()
        #             last_breaking_time = datetime.now()
        #             trigger_breaking_news()

        #         time.sleep(3)
        #         # time.sleep(300)
        #     except Exception as e:
        #         time.sleep(30)
        #         # https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt
        #         # phaqui: KeyboardInterrupt does not inherit from Exception, so that
        #         # part of your code won't ever execute
        #         if e is KeyboardInterrupt:
        #             raise e
        #         else:
        #             traceback.print_exc()


if __name__ == "__main__":
    BreakingNewsBot().loop()
