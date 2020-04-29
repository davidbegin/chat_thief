import pytest

from chat_thief.audio_command import AudioCommand
from chat_thief.models.command import Command
from pathlib import Path

commands_db_path = Path(__file__).parent.joinpath("db/commands.json")


class TestAudioCommand:
    @pytest.fixture(autouse=True)
    def clear_db(self):
        if commands_db_path.is_file():
            commands_db_path.unlink()

    @pytest.fixture
    def audio_command(self):
        def _audio_command(name):
            return AudioCommand(
                name=name, skip_validation=True, commands_db_path=commands_db_path
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
        Command("wow").allow_user("some_rando")
        assert subject.allowed_to_play("some_rando")
        assert not subject.allowed_to_play("some_other_rando")
        Command("wow").allow_user("some_other_rando")
        assert subject.allowed_to_play("some_other_rando")

    def test_permitted_users(self, audio_command):
        subject = audio_command("ha")
        assert subject.permitted_users() == []
        Command("ha").allow_user("beginbot")
        assert subject.permitted_users() == ["beginbot"]
        Command("ha").allow_user("beginbot")
        Command("ha").allow_user("some_rando")
        assert subject.permitted_users() == ["beginbot", "some_rando"]

    def test_allow_users_bug(self, audio_command):
        subject = audio_command("i3")
        assert subject.permitted_users() == []
        Command("i3").allow_user("beginbot")
        Command("i3").allow_user("beginbot")
        assert subject.permitted_users() == ["beginbot"]
        Command("i3").allow_user("fakeuser")
        other_command = audio_command("arch")
        Command("arch").allow_user("fakeuser")
        assert other_command.permitted_users() == ["fakeuser"]
        assert subject.permitted_users() == ["beginbot", "fakeuser"]
        Command("i3").allow_user("billgates")
        assert subject.permitted_users() == ["beginbot", "fakeuser", "billgates"]

    def test_allow_users(self, audio_command):
        subject = audio_command("i3")
        Command("i3").allow_user("beginbot")

        Command("i3").allow_user("fakeuser")
        other_command = audio_command("arch")
        Command("arch").allow_user("fakeuser")

        # Because of this of fakeuser having a permission
        # in both i3 and arch, adding a new user of bill gates, creates 2 i3
        # commands!
        Command("i3").allow_user("billgates")
        # Now we have 2 i3 commands
