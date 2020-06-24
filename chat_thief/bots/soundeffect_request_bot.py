from typing import List, Dict
import json
import traceback
import time

from chat_thief.config.log import logger
from chat_thief.models.soundeffect_request import SoundeffectRequest


def sync_main():
    while True:
        try:
            SoundeffectRequest.pop_all_off()
            time.sleep(1)
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
