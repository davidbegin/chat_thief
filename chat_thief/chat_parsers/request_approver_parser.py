import traceback
from typing import Optional

from dataclasses import dataclass

from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary


@dataclass
class ApprovalRequest:
    target_user: Optional[str]
    target_command: Optional[str]
    requester: str
    doc_id: Optional[int] = 1


class RequestApproverParser:
    def __init__(self, user, args=[]):
        self.user = user
        self.args = [self._sanitize(arg) for arg in args]

        self.target_user = None
        self.target_command = None
        self.doc_id = 1
        self._check_and_set()

    def parse(self):
        return ApprovalRequest(
            target_user=self.target_user,
            target_command=self.target_command,
            doc_id=self.doc_id,
            requester=self.user,
        )

    def _check_and_set(self):
        for arg in self.args:
            if self._is_user(arg):
                self.target_user = arg

            if self._is_command(arg):
                self.target_command = arg

            if self._is_valid_doc_id(arg):
                self.doc_id = int(arg)

    def _is_user(self, user):
        return user in WelcomeCommittee().present_users() or user == "random"

    # We Should Check if It exists in the DB
    def _is_valid_doc_id(self, val):
        try:
            return int(val) > 1
        except (Exception, ValueError):
            # This print tricks me when working
            # traceback.print_exc()
            return False

    def _sanitize(self, item):
        if item.startswith("!") or item.startswith("@"):
            return item[1:].lower()
        else:
            return item.lower()

    def _is_command(self, command):
        return command in SoundeffectsLibrary.fetch_soundeffect_names()
