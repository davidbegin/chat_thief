from chat_thief.chat_parsers.soundeffect_request_parser import SoundeffectRequestParser
from chat_thief.chat_parsers.request_approver_parser import RequestApproverParser
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.routers.base_router import BaseRouter
from chat_thief.config.stream_lords import STREAM_LORDS


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

        # "!approve all"
        # "!approve 1"
        # "!approve @artmattdank"
        # "!approve !new_command"
        if self.command == "approve":
            if self.user in STREAM_LORDS:

                parser = RequestApproverParser(user=self.user, args=self.args).parse()

                if parser.target_user:
                    return SoundeffectRequest.approve_user(
                        self.user, parser.target_user
                    )
                elif parser.target_command:
                    return SoundeffectRequest.approve_command(
                        self.user, parser.target_command
                    )
                elif parser.doc_id:
                    return SoundeffectRequest.approve_doc_id(self.user, parser.doc_id)
                else:
                    return "Not Sure What to Approve"

        if self.command in ["deny"]:
            if self.user in STREAM_LORDS:
                parser = RequestApproverParser(user=self.user, args=self.args).parse()
                if parser.doc_id:
                    SoundeffectRequest.deny_doc_id(self.user, parser.doc_id)
                    return f"@{self.user} DENIED Request: {parser.doc_id}"
