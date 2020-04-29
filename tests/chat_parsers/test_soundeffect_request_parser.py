import pytest

from chat_thief.chat_parsers.soundeffect_request_parser import SoundeffectRequestParser


class TestSoundeffectRequestParser:
    def test_parse(self):
        user = "fake_user"
        args = ["RzBr6wof1mw", "nice", "00:01", "00:05"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "RzBr6wof1mw"
        assert result.command == "nice"
        assert result.start_time == "00:01"
        assert result.end_time == "00:05"

        args = ["nice", "RzBr6wof1mw", "00:04", "00:08"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "RzBr6wof1mw"
        assert result.command == "nice"
        assert result.start_time == "00:04"
        assert result.end_time == "00:08"

        args = ["nice", "RzBr6wof1mw"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "RzBr6wof1mw"
        assert result.command == "nice"
        assert result.start_time == "00:00"
        assert result.end_time == "00:04"
