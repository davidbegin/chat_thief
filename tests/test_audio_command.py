import pytest

from chat_thief.audio_command import AudioCommand
from pathlib import Path


class TestAudioCommand:
    db_filepath = Path(__file__).parent.joinpath("db/test.json")

    @classmethod
    def setup_class(cls):
        if cls.db_filepath.is_file():
            cls.db_filepath.unlink()

    @pytest.fixture
    def audio_command(self):
        def _audio_command(name):
            return AudioCommand(
                name=name, skip_validation=True, db_location=self.__class__.db_filepath,
            )

        return _audio_command

    def test_creating_an_audio_command(self, audio_command):
        subject = audio_command("clap")
        assert subject.name == "clap"
        assert subject.soundfile.name == "clap.wav"
        assert not subject.is_theme_song

    def test_creating_a_theme_song_command(self, audio_command):
        subject = audio_command("artmattdank")
        assert subject.name == "artmattdank"
        assert subject.soundfile.name == "artmattdank.opus"
        assert subject.is_theme_song

    def test_theme_permissions(self, audio_command):
        subject = audio_command("artmattdank")
        assert subject.allowed_to_play("artmattdank")
        assert not subject.allowed_to_play("some_rando")
        assert not subject.allowed_to_play("beginbot")

    def test_audio_permissions(self, audio_command):
        subject = audio_command("wow")
        assert subject.allowed_to_play("artmattdank")
        assert subject.allowed_to_play("beginbot")
        assert not subject.allowed_to_play("some_rando")
        assert not subject.allowed_to_play("some_other_rando")
        subject.allow_user("some_rando")
        assert subject.allowed_to_play("some_rando")
        assert not subject.allowed_to_play("some_other_rando")
        subject.allow_user("some_other_rando")
        assert subject.allowed_to_play("some_other_rando")

    def test_permitted_users(self, audio_command):
        subject = audio_command("ha")
        assert subject.permitted_users() == []
        subject.allow_user("beginbot")
        assert subject.permitted_users() == ["beginbot"]
        subject.allow_user("beginbot")
        subject.allow_user("some_rando")
        assert subject.permitted_users() == ["beginbot", "some_rando"]

    # @pytest.mark.focus
    def test_allow_users_bug(self, audio_command):
        subject = audio_command("i3")
        assert subject.permitted_users() == []
        subject.allow_user("beginbot")
        subject.allow_user("beginbot")
        assert subject.permitted_users() == ["beginbot"]
        subject.allow_user("fakeuser")
        other_command = audio_command("arch")
        other_command.allow_user("fakeuser")
        assert other_command.permitted_users() == ["fakeuser"]
        assert subject.permitted_users() == ["beginbot", "fakeuser"]
        subject.allow_user("billgates")
        assert subject.permitted_users() == ["beginbot", "fakeuser", "billgates"]
        # other_command = audio_command("arch")
        # other_command.allow_user("fakeuser")
        # assert other_command.permitted_users() == ["fakeuser"]
        # subject = audio_command("i3")
        # assert subject.permitted_users() == ["beginbot", "fakeuser", "billgates"]

    def test_allow_users(self, audio_command):
        subject = audio_command("i3")
        subject.allow_user("beginbot")

        subject.allow_user("fakeuser")
        other_command = audio_command("arch")
        other_command.allow_user("fakeuser")

        # Because of this of fakeuser having a permission
        # in both i3 and arch, adding a new user of bill gates, creates 2 i3
        # commands!
        subject.allow_user("billgates")
        # Now we have 2 i3 commands
