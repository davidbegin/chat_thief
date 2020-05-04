import pytest

from dataclasses import dataclass

from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.irc_msg import IrcMsg
from tests.support.database_setup import DatabaseConfig


@dataclass
class FakeSoundeffectRequestParser:
    user: str
    youtube_id: str
    command: str
    start_time: str
    end_time: str


class TestSoundEffectRequest(DatabaseConfig):
    @pytest.mark.parametrize(
        "request_parser,expected",
        [
            (
                FakeSoundeffectRequestParser(
                    user="artmattdank",
                    youtube_id="VW2yff3su0U",
                    command="storm_seeker",
                    start_time="00:01",
                    end_time="00:06",
                ),
                {"auto_approved": True, "auto_approver": "artmattdank"},
            ),
            (
                FakeSoundeffectRequestParser(
                    user="fake_user",
                    youtube_id="VW2yff3su0U",
                    command="storm_seeker",
                    start_time="00:01",
                    end_time="00:06",
                ),
                {"auto_approved": False, "auto_approver": None},
            ),
        ],
    )
    def test_creating_soundeffect_requests(self, request_parser, expected):
        assert SoundeffectRequest.count() == 0

        subject = SoundeffectRequest(
            user=request_parser.user,
            command=request_parser.command,
            youtube_id=request_parser.youtube_id,
            start_time=request_parser.start_time,
            end_time=request_parser.end_time,
        )

        subject.save()
        assert SoundeffectRequest.count() == 1
        assert subject.is_auto_approved() == expected["auto_approved"]

    def test_updating_a_sound(self):
        assert SoundeffectRequest.count() == 0

        subject = SoundeffectRequest(
            user="fake_user",
            youtube_id="VW2yff3su0U",
            command="storm_seeker",
            start_time="00:01",
            end_time="00:06",
        ).save()

        assert SoundeffectRequest.count() == 1

        new_soundeffect = SoundeffectRequest(
            user="fake_user",
            youtube_id="VW2yff3su0U",
            command="storm_seeker",
            start_time="00:02",
            end_time="00:08",
        )
        new_soundeffect.save()
        assert SoundeffectRequest.count() == 1

    def test_approving(self):
        assert SoundeffectRequest.unapproved_count() == 0
        subject = SoundeffectRequest(
            user="fake_user",
            youtube_id="VW2yff3su0U",
            command="storm_seeker",
            start_time="00:01",
            end_time="00:06",
        )

        subject.save()
        assert not subject.approved
        assert SoundeffectRequest.unapproved_count() == 1
