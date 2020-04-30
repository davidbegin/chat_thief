import pytest
from pathlib import Path

from chat_thief.models.vote import Vote
from chat_thief.models.user import User
from chat_thief.models.user import Command

Command.database_folder = "tests/"
User.database_folder = "tests/"
Vote.database_folder = "tests/"

votes_db_path = Path(__file__).parent.parent.joinpath(Vote.database_path)
users_db_path = Path(__file__).parent.parent.joinpath(User.database_path)
commands_db_path = Path(__file__).parent.parent.joinpath(Command.database_path)


class TestVote:
    @pytest.fixture(autouse=True)
    def destroy_db(self):
        if votes_db_path.is_file():
            votes_db_path.unlink()
        if users_db_path.is_file():
            users_db_path.unlink()
        if commands_db_path.is_file():
            commands_db_path.unlink()
        yield

    def _create_user(self, name):
        user = User(name=name)
        user._find_or_create_user()
        return user

    def test_the_tipping_point(self):
        thugga = self._create_user("youngthug")
        bbot = self._create_user("beginbot")
        monster = self._create_user("beginbotsmonster")
        assert monster.total_users() == 3

        subject = Vote(user=thugga.name)
        threshold = int(thugga.total_users() / 2)

        Vote(user=thugga.name).vote("revolution")
        assert not subject.have_tables_turned(threshold)
        Vote(user=monster.name).vote("peace")
        assert not subject.have_tables_turned(threshold)
        Vote(user=bbot.name).vote("revolution")
        assert subject.have_tables_turned(threshold) == "revolution"

    def test_create_vote(self):
        user = "fake_user"
        subject = Vote(user=user)

        assert subject.revolution_count() == 0
        assert subject.peace_count() == 0
        assert subject.vote_count() == 0

        subject.vote("revolution")
        assert subject.vote_count() == 1
        assert subject.revolution_count() == 1
        assert subject.peace_count() == 0

        subject.vote("peace")
        assert subject.peace_count() == 1
        assert subject.revolution_count() == 0
        assert subject.vote_count() == 1
        subject = Vote(user="new_user")
        subject.vote("revolution")
        assert subject.peace_count() == 1
        assert subject.revolution_count() == 1
        assert subject.vote_count() == 2

        subject = Vote(user="new_user2")
        subject.vote("revolution")
        assert subject.revolution_count() == 2
        assert subject.vote_count() == 3
