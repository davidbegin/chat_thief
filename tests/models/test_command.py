from pathlib import Path

import pytest

from chat_thief.models.command import Command


Command.database_folder = "tests/"
db_path = Path(__file__).parent.parent.joinpath(Command.database_path)


class TestCommand:

    @pytest.fixture(autouse=True)
    def destroy_db(self):
        if db_path.is_file():
            db_path.unlink()
        yield

    def test_count(self):
        assert Command.count() == 0
        # subject = Command("help")
        # assert Command.count() == 1

    def test_allowed_to_play(self):
        subject = Command("help")
        assert subject.allowed_to_play("beginbot")

    def test_not_allowed_to_play_others_themes(self):
        subject = Command("artmattdank")
        assert subject.allowed_to_play("artmattdank")
        assert not subject.allowed_to_play("beginbot")

    @pytest.mark.focus
    def test_allow_user(self):
        subject = Command("clap")
        assert not subject.allowed_to_play("spfar")
        subject.allow_user("spfar")
        # assert subject.allowed_to_play("spfar")


    # def test_permitted_users(self, audio_command):
    #     subject = audio_command("ha")
    #     assert subject.permitted_users() == []
    #     subject.allow_user("beginbot")
    #     assert subject.permitted_users() == ["beginbot"]
    #     subject.allow_user("beginbot")
    #     subject.allow_user("some_rando")
    #     assert subject.permitted_users() == ["beginbot", "some_rando"]

    # def test_allow_users_bug(self, audio_command):
    #     subject = audio_command("i3")
    #     assert subject.permitted_users() == []
    #     subject.allow_user("beginbot")
    #     subject.allow_user("beginbot")
    #     assert subject.permitted_users() == ["beginbot"]
    #     subject.allow_user("fakeuser")
    #     other_command = audio_command("arch")
    #     other_command.allow_user("fakeuser")
    #     assert other_command.permitted_users() == ["fakeuser"]
    #     assert subject.permitted_users() == ["beginbot", "fakeuser"]
    #     subject.allow_user("billgates")
    #     assert subject.permitted_users() == ["beginbot", "fakeuser", "billgates"]

    # def test_allow_users(self, audio_command):
    #     subject = audio_command("i3")
    #     subject.allow_user("beginbot")

    #     subject.allow_user("fakeuser")
    #     other_command = audio_command("arch")
    #     other_command.allow_user("fakeuser")

    #     # Because of this of fakeuser having a permission
    #     # in both i3 and arch, adding a new user of bill gates, creates 2 i3
    #     # commands!
    #     subject.allow_user("billgates")
    #     # Now we have 2 i3 commands
