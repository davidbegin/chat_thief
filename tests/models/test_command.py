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
        other_subject = Command("damn")
        assert not subject.allowed_to_play("spfar")
        assert not subject.allowed_to_play("rando")
        assert not other_subject.allowed_to_play("spfar")
        assert not other_subject.allowed_to_play("rando")
        subject.allow_user("spfar")
        other_subject.allow_user("rando")
        assert subject.allowed_to_play("spfar")
        assert not subject.allowed_to_play("rando")
        assert not other_subject.allowed_to_play("spfar")
        assert other_subject.allowed_to_play("rando")
