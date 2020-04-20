from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.irc_msg import IrcMsg
from chat_thief.request_saver import RequestSaver
from chat_thief.sample_saver import SampleSaver

from chat_thief.new_models.soundeffect_request import SoundeffectRequest


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
        youtube_id, command, start_time, end_time = self.args

        sfx_request = SoundeffectRequest(
            user=self.user,
            youtube_id=youtube_id,
            command=command,
            start_time=start_time,
            end_time=end_time,
        ).save()

    def process_approved_soundeffects(self):
        results = self.sfx_requests_db.search(Query().approved)

        # if self.user in STREAM_GODS:
        #     requester = RequestSaver(self.user, self.msg).requester()
        #     print(f"\tRequester: {requester}")
        #     SampleSaver(
        #         user = irc_msg.user,
        #         msg = irc_msg.msg,
        #         command = irc_msg.command,
        #         args = irc_msg.args,
        #     ).save(requester)
        # else:
        #     print("Not a Stream God, so we are saving your sample @{self.user}")
        #     RequestSaver(self.user, self.msg).save()
