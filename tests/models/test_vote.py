import pytest
from pathlib import Path

from chat_thief.models.vote import Vote
votes_db_path = Path(__file__).parent.parent.joinpath("db/votes.json")
from chat_thief.models.user import User

users_db_path = Path(__file__).parent.parent.joinpath("db/users.json")
commands_db_path = Path(__file__).parent.parent.joinpath("db/commands.json")

class TestVote:

    @pytest.fixture(autouse=True)
    def destroy_db(self):
        if votes_db_path.is_file():
            votes_db_path.unlink()
        if users_db_path.is_file():
            users_db_path.unlink()
        yield

    def _create_user(self, name):
        user = User(
            name=name,
            users_db_path=users_db_path,
            commands_db_path=commands_db_path,
        )
        user._find_or_create_user()
        return user


    def test_the_tipping_point(self):
        thugga = self._create_user("youngthug")
        bbot = self._create_user("beginbot")
        monster = self._create_user("beginbotsmonster")
        assert monster.total_users() == 3

        subject = Vote(user=thugga.name, votes_db_path=votes_db_path)
        threshold = int(thugga.total_users() / 2)

        Vote(user=thugga.name, votes_db_path=votes_db_path).vote("revolution")
        assert not subject.have_tables_turned(threshold)
        Vote(user=monster.name, votes_db_path=votes_db_path).vote("peace")
        assert not subject.have_tables_turned(threshold)
        Vote(user=bbot.name, votes_db_path=votes_db_path).vote("revolution")
        assert subject.have_tables_turned(threshold) == "revolution"

    def test_create_vote(self):
        user = "fake_user"
        subject = Vote(user=user, votes_db_path=votes_db_path)

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
        subject = Vote(user="new_user", votes_db_path=votes_db_path)
        subject.vote("revolution")
        assert subject.peace_count() == 1
        assert subject.revolution_count() == 1
        assert subject.vote_count() == 2


        subject = Vote(user="new_user2", votes_db_path=votes_db_path)
        subject.vote("revolution")
        assert subject.revolution_count() == 2
        assert subject.vote_count() == 3
