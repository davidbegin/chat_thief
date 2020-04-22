import traceback
import time

from chat_thief.log import logger
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest


def sync_main():
    while True:
        try:
            PlaySoundeffectRequest("", "").pop_all_off()
            time.sleep(1)
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
