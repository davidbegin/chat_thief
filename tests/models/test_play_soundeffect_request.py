import pytest

from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.prize_dropper import random_soundeffect


class TestPlaySoundeffectRequest:
    def test_requester(self):
        pass
        # assert subject.user == "youngthug"
        # command_count = subject.command_count()
        # for _ in range(10):
        #     subject = PlaySoundeffectRequest(user="beginbot", command=random_soundeffect())
        #     subject.save()
        # assert subject.command_count() ==command_count + 1
        # subject.pop_all_off()
