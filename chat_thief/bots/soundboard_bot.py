import subprocess
import time
import traceback

from chat_thief.config.log import logger, success, warning, error
from chat_thief.irc import send_twitch_msg
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.command import Command
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.user import User
from chat_thief.audioworld.audio_player import AudioPlayer
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary
from chat_thief.config.stream_lords import STREAM_GODS


def sync_main():
    while True:
        try:
            # This deletes them from the DB
            all_effects = PlaySoundeffectRequest().pop_all_off()

            for sfx in all_effects:
                command = Command(sfx["command"])
                user = User(sfx["user"])

                command_health = 5
                # command_health = command.health()

                user_mana = user.mana()
                sfx_vote = SFXVote(command.name)

                user_allowed_to_play = command.allowed_to_play(user.name)
                public_approved = sfx_vote.is_enabled()

                if user.name in STREAM_GODS:
                    soundfile = SoundeffectsLibrary.find_sample(sfx["command"])
                    if soundfile:
                        AudioPlayer.play_sample(
                            soundfile.resolve(), sfx["notification"], user.name
                        )
                elif not public_approved:
                    msg = f"Command: '!{command.name}' silenced: {round(sfx_vote.like_to_hate_ratio(), 2)}% Love/Hate Ratio"
                    send_twitch_msg(msg)
                    warning(msg)
                elif user_allowed_to_play and command_health > 0 and user_mana > 0:
                    soundfile = SoundeffectsLibrary.find_sample(sfx["command"])

                    print(f"WE ARE TRYING TO PLAY: {soundfile}")

                    if soundfile:
                        AudioPlayer.play_sample(
                            soundfile.resolve(), sfx["notification"], user.name
                        )
                        user.update_mana(-1)
                    else:
                        warning(f"Couldn't find soundfile for {sfx['command']}")
                else:
                    if user.name not in ["beginbot", "beginbotbot"]:
                        # is the soundeffect isn't a real command
                        # don't say anything
                        msg = f"Not Playing '!{command.name}' for @{user.name} | Allowed: {user_allowed_to_play} | Mana: {user_mana}"
                        send_twitch_msg(msg)
                        warning(msg)

            # time.sleep(15)
            time.sleep(1)
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e
            else:
                traceback.print_exc()


if __name__ == "__main__":
    sync_main()
