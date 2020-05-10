import pytest

from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.prize_dropper import random_soundeffect
from tests.support.database_setup import DatabaseConfig


class TestPlaySoundeffectRequest(DatabaseConfig):
    def test_lower_casing_command(self):
        user = "uzi"
        command = "WASSUP"
        subject = PlaySoundeffectRequest(user=user, command=command)
        assert subject.command == "wassup"
