import pytest

from chat_thief.chat_parsers.soundeffect_request_parser import SoundeffectRequestParser


class TestSoundeffectRequestParser:
    def test_parse_for_bad_url(self):
        user = "fake_user"
        args = ["httpasdfsdss$@@//youtu.be/j_QLzthSkfM", "nice", "00:01", "00:05"]
        with pytest.raises(ValueError) as err_info:
            subject = SoundeffectRequestParser(user, args).parse()

    def test_parse_for_youtube_url(self):
        user = "fake_user"
        args = ["https://youtu.be/j_QLzthSkfM", "nice", "00:01", "00:05"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "https://youtu.be/j_QLzthSkfM"
        assert result.command == "nice"
        assert result.start_time == "00:01"
        assert result.end_time == "00:05"

    def test_parse_theme_song(self):
        user = "fake_user"
        args = ["RzBr6wof1mw", "00:01", "00:05"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "RzBr6wof1mw"
        assert result.command == "fake_user"
        assert result.start_time == "00:01"
        assert result.end_time == "00:05"

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

        args = ["RzBr6wof1mw"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "RzBr6wof1mw"
        assert result.command == "fake_user"
        assert result.start_time == "00:00"
        assert result.end_time == "00:04"
