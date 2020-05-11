import pytest

from chat_thief.models.issue import Issue

from tests.support.database_setup import DatabaseConfig


class TestIssue(DatabaseConfig):
    def test_new_issue(self):
        subject = Issue(user="beginbotsmonster", msg="!me doesn't work")
        assert Issue.count() == 0
        subject.save()
        assert Issue.count() == 1
