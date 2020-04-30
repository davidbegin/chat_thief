import pytest

from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.irc_msg import IrcMsg
from tests.support.database_setup import DatabaseConfig

class TestSoundEffectRequest(DatabaseConfig):
    @pytest.mark.parametrize(
        "user, soundeffect_request,expected",
        [
            (
                "artmattdank",
                "VW2yff3su0U storm_seeker 00:01 00:06",
                {
                    "user": "artmattdank",
                    "youtube_id": "VW2yff3su0U",
                    "command": "storm_seeker",
                    "start_time": "00:01",
                    "end_time": "00:06",
                },
            ),
            # "alanswenson: !soundeffect EwTZ2xpQwpA chocolaterain 00:10 00:13",
            # "zurc1010: !soundeffect XAy5cPFn9tM boomshakalaka 0:01 0:02",
            # "artmattdank: !soundeffect 0rw34Rr0goc themonarch 00:00 00:02",
            # "determin1st: !soundeffect ImyPz4tqPFU determin1st 1:15 1:20",
        ],
    )
    def test_user(self, user, soundeffect_request, expected):
        pass
        # subject = SoundeffectRequest(user=user, soundeffect_request=soundeffect_request)
        # assert subject.user == expected["user"]
        # assert subject.youtube_id == expected["youtube_id"]
        # assert subject.command == expected["command"]
        # assert subject.start_time == expected["start_time"]
        # assert subject.end_time == expected["end_time"]

        # So we should check if valid
        # and save
        # and be able to bring back up
