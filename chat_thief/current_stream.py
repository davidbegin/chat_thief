import random
import traceback

from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.chat_logs import ChatLogs

# WTF
INVALID_USERS = ["nightbot", ".tim.twitch.tv"] + STREAM_GODS


class CurrentStream:
    @staticmethod
    def random_user(blacklisted_users=[]):
        try:
            looking_for_user = True
            invalid_users = INVALID_USERS + blacklisted_users
            users = ChatLogs().recent_stream_peasants()

            while looking_for_user:
                user = random.sample(users, 1)[0]
                if user not in invalid_users:
                    looking_for_user = False

            return user
        except:
            traceback.print_exc()
            return None
