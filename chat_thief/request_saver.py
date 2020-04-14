from pathlib import Path

from chat_thief.irc import send_twitch_msg


BLACKLISTED_REQUESTERS = ["beginbotbot"]

SOUNDEFFECT_REQUESTS_PATH = Path(__file__).parent.parent.joinpath(".requests")

BEGINS_PROMISE_TO_YOU = """
@{self.user} thank you for your patience in this trying time,
beginbot is doing all he can to ensure your safety during this COVID-19 situation.
Your request will be processed by a streamlord in due time thanks
"""


class RequestSaver:
    def __init__(self, user, msg):
        self.msg = msg
        self.user = user

        if not SOUNDEFFECT_REQUESTS_PATH.is_file():
            SOUNDEFFECT_REQUESTS_PATH.touch()

    # TODO: Themes don't go to theme folder
    def save(self):
        request_to_save = self.user + " " + self.msg

        # TODO: Make these messages configurable, aka turn them off
        if request_to_save in self._previous_requests():
            send_twitch_msg(f"Thank you @{self.user} we already have that request")
        else:
            if self.user not in BLACKLISTED_REQUESTERS:
                print(f"Saving Request: {request_to_save}")
                send_twitch_msg(BEGINS_PROMISE_TO_YOU)
                with open(SOUNDEFFECT_REQUESTS_PATH, "a") as f:
                    f.write(request_to_save + "\n")

    def _previous_requests(self):
        return SOUNDEFFECT_REQUESTS_PATH.read_text().split("\n")
