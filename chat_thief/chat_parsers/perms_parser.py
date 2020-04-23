from typing import Optional

from dataclasses import dataclass

@dataclass
class PermsRequest:
    target_user: Optional[str]
    target_command: Optional[str]
    requester: str

class PermsParser:
    def __init__(self, user, args=[]):
        self.user = user
        self.args = args

        self._set_target_user_and_command()

    def parse(self):
        return PermsRequest(
            target_user=self.target_user,
            target_command=self.target_command,
            requester=self.user
        )

    def _set_target_user_and_command(self):
        self.target_user = None
        self.target_command = self.args[1]
