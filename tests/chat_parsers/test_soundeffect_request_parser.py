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
        args = ["https://youtu.be/j_QLzthSkfM", "00:01", "00:05"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "https://youtu.be/j_QLzthSkfM"
        assert result.command == "fake_user"
        assert result.start_time == "00:01"
        assert result.end_time == "00:05"

    def test_parse(self):
        user = "fake_user"
        args = ["https://youtu.be/j_QLzthSkfM", "nice", "00:01", "00:05"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "https://youtu.be/j_QLzthSkfM"
        assert result.command == "nice"
        assert result.start_time == "00:01"
        assert result.end_time == "00:05"

        args = ["nice", "https://youtu.be/j_QLzthSkfM", "00:04", "00:08"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "https://youtu.be/j_QLzthSkfM"
        assert result.command == "nice"
        assert result.start_time == "00:04"
        assert result.end_time == "00:08"

        args = ["nice", "https://youtu.be/j_QLzthSkfM"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "https://youtu.be/j_QLzthSkfM"
        assert result.command == "nice"
        assert result.start_time == "00:00"
        assert result.end_time == "00:04"

        args = ["https://youtu.be/j_QLzthSkfM"]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.youtube_id == "https://youtu.be/j_QLzthSkfM"
        assert result.command == "fake_user"
        assert result.start_time == "00:00"
        assert result.end_time == "00:04"

    def test_wacky_stupac_url(self):
        user = "stupac"
        args = [
            "https://www.youtube.com/watch?v=gSHf_b6AWKc",
            "wannabefast",
            "00:29",
            "00:32",
        ]
        subject = SoundeffectRequestParser(user, args)
        result = subject.parse()
        assert result.command == "wannabefast"
        assert result.youtube_id == "https://www.youtube.com/watch?v=gSHf_b6AWKc"
        assert result.start_time == "00:29"
        assert result.end_time == "00:32"
