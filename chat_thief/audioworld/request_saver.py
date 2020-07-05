from pathlib import Path
from typing import List

from chat_thief.irc import send_twitch_msg


BLACKLISTED_REQUESTERS: List[str] = []
SOUNDEFFECT_REQUESTS_PATH = Path(__file__).parent.parent.parent.joinpath("db/.requests")


def begins_promise(user):
    return """
    @{user} thank you for your patience in this trying time,
    beginbot is doing all he can to ensure your safety during this COVID-19 situation.
    Your request will be processed by a streamlord in due time thanks
    """


# We need a method that deletes previous requests
class RequestSaver:
    def __init__(self, user, msg):
        self.user = user
        self.msg = msg

        if not SOUNDEFFECT_REQUESTS_PATH.is_file():
            SOUNDEFFECT_REQUESTS_PATH.touch()

    def requester(self):
        previous_requests = RequestSaver.previous_requests()
        print(f"{self.msg=}")
        for request in previous_requests:
            print(f"Request: {request}")
            if self.msg in request:

                return request.split(" ")[0]

    # TODO: Themes don't go to theme folder
    def save(self):
        previous_requests = RequestSaver.previous_requests()

        request_to_save = self.user + " " + self.msg
        print(f"\n\nPrevious Request: {previous_requests}")
        print(f"Saving Request: {request_to_save}")

        # TODO: Make these messages configurable, aka turn them off
        if request_to_save in previous_requests:
            send_twitch_msg(f"Thank you @{self.user} we already have that request")
            pass
        else:
            if self.user not in BLACKLISTED_REQUESTERS:
                send_twitch_msg(begins_promise(self.user))
                with open(SOUNDEFFECT_REQUESTS_PATH, "a") as f:
                    f.write(request_to_save + "\n")

    @staticmethod
    def previous_requests():
        return SOUNDEFFECT_REQUESTS_PATH.read_text().strip().split("\n")
