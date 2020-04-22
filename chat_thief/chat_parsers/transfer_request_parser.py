from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.welcome_file import WelcomeFile
from dataclasses import dataclass
from typing import List

@dataclass
class TransferRequest:
    target_user : str
    target_command : str
    transferer : str


class TransferRequestParser:
    def __init__(self, user, args):
        self.transferer = user
        self.args = args

        if len(self.args) != 2:
            raise ValueError("Not enough args to transfer")

        self._set_target_user_and_command()

    def parse(self):
        return TransferRequest(
            target_user=self.target_user,
            target_command=self._sanitize_arg(self.target_command),
            transferer=self.transferer,
        )

    def _set_target_user_and_command(self):
        cool_person = self._sanitize_arg(self.args[0])

        if cool_person in WelcomeFile.present_users():
            self.target_user = cool_person
            self.target_command = self.args[1]
            return

        cool_person = self._sanitize_arg(self.args[1])

        if cool_person in WelcomeFile.present_users():
            self.target_user = cool_person
            self.target_command = self.args[0]

    def _sanitize_arg(self, arg):
        if arg.startswith("@") or arg.startswith("!"):
            arg = arg[1:]
        return arg.lower()
