from typing import List, Dict
import json
import traceback
import time

from chat_thief.log import logger
from chat_thief.audio_command import AudioCommand
from chat_thief.new_models.soundeffect_request import SoundeffectRequest
from chat_thief.chat_logs import ChatLogs
from chat_thief.user import User


def sync_main():
    while True:
        try:
            for peasant in ChatLogs().recent_stream_peasants():
                print(peasant)
                user = User(peasant)
                user.add_street_cred()
                user = User("beginbotbot")
                user.add_street_cred()

            # This needs to be something that just looks for chatters in the
            # last 100 messages
            # and gives them cred
            # This obviously needs a longer sleep
            time.sleep(5)
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
