from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.irc_msg import IrcMsg
from chat_thief.request_saver import RequestSaver
from chat_thief.sample_saver import SampleSaver


class AudioCommandCenter:
    """
    In charge of saving new audio samples, and requests
    """

    def __init__(self, irc_msg: IrcMsg) -> None:
        self.irc_msg = irc_msg
        self.user = irc_msg.user
        self.msg = irc_msg.msg
        self.command = irc_msg.command
        self.args = irc_msg.args

    def add_command(self):
        # Here are the two spots where we either
        # Add a request or we save
        # if we are saving
        # We want extract the requester
        if self.user in STREAM_GODS:
            requester = RequestSaver(self.user, self.msg).requester()
            print(f"\n\tREQUESTER: {requester}\n\n")
            SampleSaver(self.irc_msg).save(requester)
        else:
            print("Not a Streamlord, so we are attempting to save you sample")
            RequestSaver(self.user, self.msg).save()
