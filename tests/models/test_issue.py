import pytest

from chat_thief.models.issue import Issue


class TestIssue:
    def test_new_issue(self):
        subject = Issue(user="beginbotsmonster", msg="!me doesn't work")
        # assert Issue.count() == 0
        # subject.save()
        # assert Issue.count() == 1
