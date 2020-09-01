from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.models.user_code import UserCode
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary


class StitchAndSort:
    def __init__(self):
        self._all_votes = SFXVote.db().all()
        self._all_users = User.db().all()
        self._all_cmds = Command.db().all()
        self._all_sfxs = SoundeffectsLibrary.fetch_soundeffect_samples()
        self.command_users = self._setup_command_users()

    def call(self):
        cmd_data = self._cmd_data()
        user_data = self._user_data()
        return {"commands": cmd_data, "users": user_data}

    def _user_data(self):
        results = []

        # Iterate through each user
        for user_dict in self._all_users:

            widgets = UserCode.js_for_user(user_dict["name"])
            user_dict["widgets"] = widgets

            # Looking for Matching Soundeffects
            matching_effects = [
                sfx
                for sfx in self._all_sfxs
                if user_dict["name"] == sfx.name[: -len(sfx.suffix)]
            ]
            if matching_effects:
                command_file = matching_effects[0]
                user_dict["command_file"] = command_file.name

            if user_dict["name"] in self.command_users:
                command_info = self.command_users[user_dict["name"]]["commands"]
                total_propery_value = sum([command["cost"] for command in command_info])
                user_dict["wealth"] = user_dict.get("cool_points", 0) + total_propery_value

            # This small change to have all the command info
            user_dict["commands"] = [
                cmd
                for cmd in self._all_cmds
                if user_dict["name"] in cmd["permitted_users"]
            ]

            user_dict["sfx_count"] = len(user_dict["commands"])

            results.append(user_dict)
        return list(reversed(sorted(results, key=lambda user: user.get("wealth", 0))))

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
        return list(
            reversed(sorted(results, key=lambda command: command.get("cost", 0)))
        )

    def _setup_command_users(self):
        command_users = {}
        for command in self._all_cmds:
            for user in command["permitted_users"]:
                if user not in command_users:
                    command_users[user] = {"commands": []}
                command_users[user]["commands"].append(command)
        return command_users
