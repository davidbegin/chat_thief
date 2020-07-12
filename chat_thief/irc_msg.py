from typing import List, Optional


class IrcMsg:
    def __init__(self, msg: str):
        # ':beginbot!beginbot@beginbot.tmi.twitch.tv PRIVMSG #beginbot :hello'

        split_msg = msg.split()
        if len(split_msg) >= 4:
            user_info, _, _, *raw_msg = split_msg
            self.user: str = user_info.split("!")[0][1:]
            self.msg: str = self._msg_sanitizer(raw_msg)
            self.command: Optional[str] = self._set_command()
            self.args: List[str] = self._set_args()
        else:
            raise ValueError(f"WHAT THE HECK: {msg}")

    def _msg_sanitizer(self, msg: List[str]) -> str:
        first, *rest = msg
        return f"{first[1:]} {' '.join(rest)}".strip()

    def _set_command(self) -> Optional[str]:
        args = self.msg.split(" ")
        if self.is_command():
            return args[0][1:].lower()
        else:
            return None

    def _set_args(self) -> List[str]:
        args = self.msg.split(" ")
        if len(args) > 1:
            return args[1:]
        else:
            return []

    def is_command(self) -> bool:
        return self.msg[0] == "!" and self.msg[1] != "!"
