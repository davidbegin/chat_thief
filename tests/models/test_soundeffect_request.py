import pytest

from dataclasses import dataclass

from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.irc_msg import IrcMsg
from tests.support.database_setup import DatabaseConfig


class FakeTinyDbResult:
    def __init__(self, data):
        self._data = data
        self.doc_id = self._data["doc_id"]

    def __getitem__(self, key):
        return self._data[key]


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

    def test_stats(self, monkeypatch):
        # See Our Object is annoying!!!
        # We need a better way of saving these requests!
        unapproved = [
            FakeTinyDbResult(
                {
                    "requester": "c4tfive",
                    "approver": None,
                    "approved": False,
                    "youtube_id": "qs7f3ssuEjA",
                    "command": "tootsie",
                    "start_time": "00:02",
                    "end_time": "00:6",
                    "doc_id": 3,
                }
            ),
            FakeTinyDbResult(
                {
                    "requester": "kevinsjoberg",
                    "approver": None,
                    "approved": False,
                    "youtube_id": "b1E9ucBTHsg",
                    "command": "@kevinsjoberg",
                    "start_time": "00:48",
                    "end_time": "00:53",
                    "doc_id": 2,
                }
            ),
            FakeTinyDbResult(
                {
                    "requester": "whatsinmyopsec",
                    "approver": None,
                    "approved": False,
                    "youtube_id": "sYPrBZFGkMM",
                    "command": "bullyme",
                    "start_time": "0:04",
                    "end_time": "0:09",
                    "doc_id": 1,
                }
            ),
        ]

        monkeypatch.setattr(SoundeffectRequest, "unapproved", lambda: unapproved)
        result = SoundeffectRequest.stats()

        expected = {
            "kevinsjoberg": {
                2: {
                    "name": "@kevinsjoberg",
                    "youtube": "https://youtu.be/b1E9ucBTHsg?t=48",
                    "time": "00:48 - 00:53",
                }
            },
            "c4tfive": {
                3: {
                    "name": "tootsie",
                    "youtube": "https://youtu.be/qs7f3ssuEjA?t=2",
                    "time": "00:02 - 00:6",
                }
            },
            "whatsinmyopsec": {
                1: {
                    "name": "bullyme",
                    "youtube": "https://youtu.be/sYPrBZFGkMM?t=4",
                    "time": "0:04 - 0:09",
                }
            },
        }

        assert result == expected

    def test_approve_all(self):
        user = "fake_user"
        results = SoundeffectRequest.approve_all(approver=user)

    def test_approve_command(self):
        command = "fake_command"
        user = "fake_user"
        results = SoundeffectRequest.approve_command(user, command)

    def test_approve_user(self):
        user = "fake_user"
        target_user = "other_user"
        results = SoundeffectRequest.approve_user(user, target_user)

    def test_approve_doc_id(self):
        user = "fake_user"
        doc_id = 1
        SoundeffectRequest.approve_doc_id(user, doc_id)

    def test_deny_doc_id_when_request_is_not_real(self):
        user = "fake_user"
        doc_id = 1
        # We expect this to throw an error
        SoundeffectRequest.deny_doc_id(user, doc_id)

    def test_deny_doc_id(self):
        subject = SoundeffectRequest(
            user="beginbotsmonter",
            command="damn",
            youtube_id="VW2yff3su0U",
            start_time="00:01",
            end_time="00:05",
        )
        subject.save()
        request = SoundeffectRequest.get(command="damn")
        SoundeffectRequest.deny_doc_id("denier", request.doc_id)
        assert "damn" not in [
            request["command"] for request in SoundeffectRequest.all()
        ]
