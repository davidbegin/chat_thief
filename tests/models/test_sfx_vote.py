from pathlib import Path

import pytest

from chat_thief.models.sfx_vote import SFXVote

SFXVote.database_folder = "tests/"
db_path = Path(__file__).parent.parent.joinpath(SFXVote.database_path)


class TestSFXVote:
    @pytest.fixture(autouse=True)
    def destroy_db(self):
        if db_path.is_file():
            db_path.unlink()
        yield

    def test_sfx_vote(self):
        SFXVote.count() == 0

    @pytest.mark.focus
    def test_create_sfx_vote(self):
        subject = SFXVote(command="clap")
        subject.support("thugga")
        SFXVote.count() == 1
        assert subject.supporter_count() == 1
        assert subject.detractor_count() == 0
        assert subject.is_enabled()
        subject.detract("bill")
        assert subject.detractor_count() == 1
        SFXVote.count() == 1
        assert not subject.is_enabled()
