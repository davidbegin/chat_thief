import pytest
from pathlib import Path

from chat_thief.models.vote import Vote
votes_db_path = Path(__file__).parent.parent.joinpath("db/votes.json")

class TestVote:
    @pytest.fixture(autouse=True)
    def destroy_db(self):
        if votes_db_path.is_file():
            votes_db_path.unlink()
        yield


    @pytest.mark.focus
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
