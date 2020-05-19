from chat_thief.chat_parsers.soundeffect_request_parser import SoundeffectRequestParser
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.routers.base_router import BaseRouter


class FeedbackRouter(BaseRouter):
    def route(self):
        if self.command == "soundeffect":
            sfx_request = SoundeffectRequestParser(self.user, self.args)

            return SoundeffectRequest(
                user=self.user,
                youtube_id=sfx_request.youtube_id,
                command=sfx_request.command,
                start_time=sfx_request.start_time,
                end_time=sfx_request.end_time,
            ).save()
