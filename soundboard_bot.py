import subprocess
import time
import traceback

from chat_thief.config.log import logger, success, warning, error
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.command import Command
from chat_thief.models.user import User
from chat_thief.audio_player import AudioPlayer
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.config.stream_lords import STREAM_GODS


def sync_main():
    while True:
        try:
            # This deletes them from the DB
            all_effects = PlaySoundeffectRequest().pop_all_off()

            # if all_effects:
            #     subprocess.call("clear")

            for sfx in all_effects:

                command = Command(sfx["command"])
                user = User(sfx["user"])

                command_health = 5
                # command_health = command.health()
                user_mana = user.mana()
                user_allowed_to_play = command.allowed_to_play(user.name)

                if user.name in STREAM_GODS:
                    soundfile = SoundeffectsLibrary.find_sample(sfx["command"])
                    if soundfile:
                        AudioPlayer.play_sample(
                            soundfile.resolve(), sfx["notification"]
                        )

                elif user_allowed_to_play and command_health > 0 and user_mana > 0:
                    soundfile = SoundeffectsLibrary.find_sample(sfx["command"])
                    if soundfile:
                        AudioPlayer.play_sample(
                            soundfile.resolve(), sfx["notification"]
                        )
                        user.update_mana(-1)
                    else:
                        warning(f"Couldn't find soundfile for {sfx['command']}")
                else:
                    error(
                        f"\nNot Playing: !{command.name} for @{user.name} | Allowed: {user_allowed_to_play}"
                    )
                    error(f"\tUser Mana {user_mana} | Command Health {command_health}")

            # time.sleep(15)
            time.sleep(1)
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
