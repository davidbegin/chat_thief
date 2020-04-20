from typing import List, Dict
import json
import asyncio
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
        except:
            traceback.print_exc()


async def main():
    await asyncio.gather(run_bot())


def sync_main():
    while True:
        PlaySoundeffectRequest("", "").pop_all_off()
        time.sleep(1)


if __name__ == "__main__":
    # asyncio.run(main())
    sync_main()
