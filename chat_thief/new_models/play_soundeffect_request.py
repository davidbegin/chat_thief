
from tinydb import Query

from chat_thief.database import db_table, USERS_DB_PATH, COMMANDS_DB_PATH
from chat_thief.audio_command import AudioCommand


class PlaySoundeffectRequest:

    def __init__(self, user, command):
        self.user = user
        self.command = command
        play_soundeffect_requests_db_path="db/play_soundeffects.json"
        self.play_sfx_db = db_table(play_soundeffect_requests_db_path, "play_soundeffects")

    def save(self):
        print(f"Creating New Play SFX Request: {self.doc()}")
        self.play_sfx_db.insert(self.doc())
        return self.doc()

    def command_count(self):
        return len(self.play_sfx_db)

    def doc(self):
        return {
            "user": self.user,
            "command": self.command,
        }

    def pop_all_off(self):
        all_effects = self.play_sfx_db.all()
        doc_ids_to_delete = [ sfx.doc_id for sfx in all_effects ]
        if doc_ids_to_delete:
            print(f"Doc IDs being deleted: {doc_ids_to_delete}")
        self.play_sfx_db.remove(doc_ids=doc_ids_to_delete)

        for sfx in all_effects:
            print(sfx)
            audio_command = AudioCommand(name=sfx["command"])
            if audio_command.allowed_to_play(sfx["user"]):
                audio_command.play_sample()
            else:
                print(f"{sfx['user']} not allowed to play: {sfx['command']}")


    # def commands(self):
        # def in_permitted_users(permitted_users, current_user):
        #     return current_user in permitted_users

        # command_permissions = [
        #     permission["command"]
        #     for permission in self.commands_db.search(
        #         Query().permitted_users.test(in_permitted_users, self.name)
        #     )
        # ]
        # return command_permissions

    # def add_street_cred(self):
        # user = self._find_or_create_user()

        # def increase_cred():
        #     def transform(doc):
        #         doc["street_cred"] = doc["street_cred"] + 1

        #     return transform

        # self.users_db.update(increase_cred(), Query().name == self.name)
