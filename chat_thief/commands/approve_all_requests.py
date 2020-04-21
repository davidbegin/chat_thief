from chat_thief.new_models.soundeffect_request import SoundeffectRequest


class ApproveAllRequests:
    @staticmethod
    def approve(approver, requester):
        requests = SoundeffectRequest("", "", "", "", "").approve_all_for_user(approver, requester)

        return requests
