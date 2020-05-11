from chat_thief.models.base_model import BaseModel


class Issue(BaseModel):
    def __init__(self, user, msg):
        self._user = user
        self._msg = msg

    def save(self):
        pass
