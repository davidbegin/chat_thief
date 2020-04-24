import traceback
import time

from chat_thief.config.log import logger
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.audio_command import AudioCommand


def sync_main():
    while True:
        try:
            all_effects = PlaySoundeffectRequest().pop_all_off()
            for sfx in all_effects:
                print(sfx)
                audio_command = AudioCommand(name=sfx["command"])
                if audio_command.allowed_to_play(sfx["user"]):
                    audio_command.play_sample(remove_health=True)
                else:
                    print(f"{sfx['user']} not allowed to play: {sfx['command']}")
            time.sleep(1)
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
