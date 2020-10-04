from chat_thief.chat_parsers.soundeffect_request_parser import SoundeffectRequestParser
from chat_thief.chat_parsers.request_approver_parser import RequestApproverParser
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.routers.base_router import BaseRouter
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.config.help_menu import HELP_COMMANDS
from chat_thief.models.issue import Issue


class FeedbackRouter(BaseRouter):
    def route(self):
        if self.command in ["soundeffect", "sound"]:
            try:
                sfx_request = SoundeffectRequestParser(self.user, self.args).parse()
            except Exception as e:
                return f'@{self.user} Correct Syntax: {HELP_COMMANDS["soundeffect"]}'

            SoundeffectRequest(
                user=self.user,
                youtube_id=sfx_request.youtube_id,
                command=sfx_request.command,
                start_time=sfx_request.start_time,
                end_time=sfx_request.end_time,
            ).save()

            return f"Thank you for your request @{self.user}, beginbotbot will inform you when !{sfx_request.command} is available"

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

        if self.command in ["issue", "bug", "feature"]:
            if self.args:
                msg = " ".join(self.args)
                issue = Issue(user=self.user, msg=msg).save()
                return f"Thank You @{self.user} for your feedback, we will review and get back to you shortly"
            else:
                return f"@{self.user} Must include a description of the !issue"

        if self.command == "delete_issue" and self.user in STREAM_GODS:
            parser = RequestApproverParser(user=self.user, args=self.args).parse()

            if parser.doc_id:
                Issue.delete(parser.doc_id)
                return f"Issue: {parser.doc_id} Deleted "

        if self.command == "issues" and self.user in STREAM_GODS:
            return [
                f"@{issue['user']} ID: {issue.doc_id} - {issue['msg']}"
                for issue in Issue.all()
            ]

        if self.command == "requests":
            stats = SoundeffectRequest.formatted_stats()
            if not stats:
                stats = "Excellent Job Stream Lords No Requests!"
            return stats
