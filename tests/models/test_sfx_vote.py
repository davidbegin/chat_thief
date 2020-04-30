from pathlib import Path

import pytest

from chat_thief.models.sfx_vote import SFXVote
from tests.support.database_setup import DatabaseConfig

class TestSFXVote(DatabaseConfig):

    def test_sfx_vote(self):
        SFXVote.count() == 0

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
