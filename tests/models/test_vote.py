import pytest
from pathlib import Path

from chat_thief.models.vote import Vote
from chat_thief.models.user import User
from chat_thief.models.user import Command
from tests.support.database_setup import DatabaseConfig

class TestVote(DatabaseConfig):

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
