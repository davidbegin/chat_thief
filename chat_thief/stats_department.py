from chat_thief.models.user import User
from chat_thief.models.the_fed import TheFed
from chat_thief.models.command import Command


class StatsDepartment:
    def stats(self):
        all_users = User.db().all()
        all_cmds = Command.db().all()

        total_cool_points = sum([user["cool_points"] for user in all_users])
        total_street_cred = sum([user["street_cred"] for user in all_users])
        fed_reserve = TheFed.reserve()
        total_user_sfx_property = sum(
            [
                cmd["cost"] * len(cmd["permitted_users"])
                for cmd in all_cmds
                if len(cmd["permitted_users"]) > 0

            ]
        )

        return {
            "total_street_cred": total_street_cred,
            "total_cool_points": total_cool_points,
            "fed_reserve": fed_reserve,
            "total_user_sfx_property": total_user_sfx_property,
        }
