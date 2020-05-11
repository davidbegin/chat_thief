from typing import List


class IrcMsg:
    def __init__(self, msg: str):
        user_info, _, _, *raw_msg = msg
        self.user = user_info.split("!")[0][1:]
        self.msg = self._msg_sanitizer(raw_msg)
        self.command = self._set_command()
        self.args = self._set_args()

    def _msg_sanitizer(self, msg: List[str]) -> str:
        first, *rest = msg
        return f"{first[1:]} {' '.join(rest)}".strip()

    def _set_command(self) -> None:
        args = self.msg.split(" ")
        if self.is_command():
            return args[0][1:].lower()

    def _set_args(self) -> List[str]:
        args = self.msg.split(" ")
        if len(args) > 1:
            return args[1:]
        else:
            return []

    def is_command(self) -> bool:
        return self.msg[0] == "!" and self.msg[1] != "!"
