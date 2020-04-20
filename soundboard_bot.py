from typing import List, Dict
import json
import traceback
import time

from chat_thief.log import logger
from chat_thief.audio_command import AudioCommand
from chat_thief.new_models.play_soundeffect_request import PlaySoundeffectRequest


async def run_bot() -> None:
    while True:
        try:
            PlaySoundeffectRequest("", "").pop_all_off()
            time.sleep(1)
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


def sync_main():
    while True:
        PlaySoundeffectRequest("", "").pop_all_off()
        time.sleep(1)


if __name__ == "__main__":
    sync_main()
