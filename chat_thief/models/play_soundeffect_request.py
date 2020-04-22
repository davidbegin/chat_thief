import json
import traceback
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
        if self._is_valid_json():
            print(f"Creating New Play SFX Request: {self.doc()}")
            self.play_sfx_db.insert(self.doc())
            return self.doc()
        else:
            return f"There was an issue with {self.doc()}"

    def command_count(self):
        # We should check if this is valid json
        return len(self.play_sfx_db)

    def _is_valid_json(self):
        try:
            json.dumps(self.doc())
            return True
        except:
            traceback.print_exc()
            return False

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
