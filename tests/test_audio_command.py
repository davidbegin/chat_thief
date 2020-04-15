import pytest

from chat_thief.audio_command import AudioCommand


class TestAudioCommand:
    def test_creating_an_audio_command(self):
        subject = AudioCommand("clap")
        assert subject.name == "clap"
        assert subject.soundfile.name == "clap.wav"
        assert not subject.is_theme_song

    def test_creating_a_theme_song_command(self):
        subject = AudioCommand("artmattdank")
        assert subject.name == "artmattdank"
        assert subject.soundfile.name == "artmattdank.opus"
        assert subject.is_theme_song
