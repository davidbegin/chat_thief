class CommandParser():
    # TODO: Add Default Logger
    def __init__(self, irc_msg, logger):
        self._irc_msg = irc_msg
        self._logger = logger
        user_info, _, _, *raw_msg = self._irc_msg 
        self.user = user_info.split("!")[0][1:]
        self.msg = self._msg_sanitizer(raw_msg)

    def print_msg(self):
        self._logger.info(f"{self.user}: {self.msg}")

    # We hate this name!
    def build_response(self):
        self.print_msg()
        if self._is_command_msg():
            command = self.msg[1:].split()[0]
            if self.msg.split()[0].lower() == "!so":
                return self.shoutout()

    def _msg_sanitizer(self, msg):
       first, *rest = msg
       return f"{first[1:]} {' '.join(rest)}"

    def _is_command_msg(self):
        return self.msg[0] == "!" and self.msg[1] != "!"

    def shoutout(self):
        msg_segs = self.msg.split()
        
        if len(msg_segs) > 1 and msg_segs[1].startswith("@"):
            return f"Shoutout twitch.tv/{msg_segs[1][1:]}"
        else:
            return f"Shoutout twitch.tv/{msg_segs[1]}"
