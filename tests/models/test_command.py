from pathlib import Path

import pytest

from chat_thief.models.command import Command

Command.database_folder = "test/"
db_path = Path(__file__).parent.parent.joinpath(Command.database_path)


# This is stupid as the its going to wrong place always
Command.database_folder = "tests/"

class TestCommand:

    @pytest.fixture(autouse=True)
    def destroy_db(self):
        if db_path.is_file():
            db_path.unlink()
            # db_path.touch()
        yield

    @pytest.mark.focus
    def test_count(self):
        assert Command.count() == 0

    # What are the main methods we want to move
    # from AudioCommand?
    @pytest.mark.focus
    def test_allowed_to_play(self):
        subject = Command("help")
        assert subject.allowed_to_play("beginbot")

    @pytest.mark.focus
    def test_not_allowed_to_play_others_themes(self):
        subject = Command("artmattdank")
        assert subject.allowed_to_play("artmattdank")
        assert not subject.allowed_to_play("beginbot")
