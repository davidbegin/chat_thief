from chat_thief.new_models.soundeffect_request import SoundeffectRequest


class ApproveAllRequests:
    @staticmethod
    def approve(user):
        requests = SoundeffectRequest("", "", "", "", "").approve_all_for_user(user)

        return requests
