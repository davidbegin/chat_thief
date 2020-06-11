from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.soundeffects_library import SoundeffectsLibrary


class StitchAndSort:
    def __init__(self):
        self._all_votes = SFXVote.db().all()
        self._all_users = User.db().all()
        self._all_cmds = Command.db().all()
        self._all_sfxs = SoundeffectsLibrary.fetch_soundeffect_samples()

    def call(self):
        user_data = self._user_data()
        cmd_data = self._cmd_data()

        return {"commands": cmd_data, "users": user_data}

    def _user_data(self):
        results = []

        for user_dict in self._all_users:
            matching_effects = [
                sfx
                for sfx in self._all_sfxs
                if user_dict["name"] == sfx.name[: -len(sfx.suffix)]
            ]

            if matching_effects:
                command_file = matching_effects[0]
                user_dict["command_file"] = command_file.name

            user_dict["commands"] = [
                cmd["name"]
                for cmd in self._all_cmds
                if user_dict["name"] in cmd["permitted_users"]
            ]
            results.append(user_dict)
        return results

    def _cmd_data(self):
        results = []

        for cmd_dict in self._all_cmds:
            sfx_vote = next(
                (
                    vote
                    for vote in self._all_votes
                    if vote["command"] == cmd_dict["name"]
                ),
                None,
            )

            matching_effects = [
                sfx
                for sfx in self._all_sfxs
                if cmd_dict["name"] == sfx.name[: -len(sfx.suffix)]
            ]
            if matching_effects:
                command_file = matching_effects[0]
                cmd_dict["command_file"] = command_file.name

            if sfx_vote:
                supporters = sfx_vote["supporters"]
                detractors = sfx_vote["detractors"]
                total = len(supporters) + len(detractors)
                if total > 0:
                    cmd_dict["like_to_hate_ratio"] = total * 100
                else:
                    cmd_dict["like_to_hate_ratio"] = 100
            else:
                cmd_dict["like_to_hate_ratio"] = 100

            results.append(cmd_dict)
        return results
