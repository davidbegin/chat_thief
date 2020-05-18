from chat_thief.commands.la_libre import LaLibre
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS


class BasicInfoRouter:
    def __init__(self, command, args=[]):
        self.command = command
        self.args = args

    def route(self):
        if self.command == "la_libre":
            return LaLibre.inform()

        if self.command == "streamlords":
            return " ".join(STREAM_LORDS)

        if self.command == "streamgods":
            return " ".join(STREAM_GODS)

        if self.command == "so":
            return self._shoutout()

    def _shoutout(self):
        return f"Shoutout twitch.tv/{self.args[0]}"

    # def _process_command(self):
    #     if self.command == "delete_issue" and self.user in STREAM_GODS:
    #         parser = RequestApproverParser(user=self.user, args=self.args).parse()

    #         if parser.doc_id:
    #             Issue.delete(parser.doc_id)
    #             return f"Issue: {parser.doc_id} Deleted "

    #     if self.command == "issues":
    #         return [
    #             f"@{issue['user']} ID: {issue.doc_id} - {issue['msg']}"
    #             for issue in Issue.all()
    #         ]

    #     if self.command == "requests":
    #         stats = SoundeffectRequest.formatted_stats()
    #         if not stats:
    #             stats = "Excellent Job Stream Lords No Requests!"
    #         return stats

    #     if self.command == "most_popular":
    #         return " | ".join(Command.most_popular())

    #     if self.command in ["economy"]:
    #         cool_points = User(self.user).total_cool_points()
    #         return f"Total Cool Points in Market: {cool_points}"

    #     if self.command in ["all_bets", "all_bet", "bets"]:
    #         return " | ".join([f"@{bet[0]}: {bet[1]}" for bet in CubeBet.all_bets()])

    #     # -------------------------
    #     # No Random Command or User
    #     # -------------------------

    #     if self.command in ["me"]:
    #         parser = PermsParser(user=self.user, args=self.args).parse()

    #         user_permissions = " ".join(
    #             [f"!{perm}" for perm in User(self.user).commands()]
    #         )
    #         stats = User(self.user).stats()
    #         if user_permissions:
    #             return f"{stats} | {user_permissions}"
    #         else:
    #             return stats

    #     # ------------
    #     # Takes a User
    #     # ------------

    #     if self.command == "donate":
    #         parser = PermsParser(user=self.user, args=self.args).parse()
    #         if parser.target_user:
    #             return Donator(self.user).donate(parser.target_user)
    #         else:
    #             return Donator(self.user).donate()

    #     if self.command == "bankrupt":
    #         parser = PermsParser(user=self.user, args=self.args).parse()
    #         if self.user in STREAM_GODS:
    #             return User(parser.target_user).bankrupt()

    #     if self.command == "paperup":
    #         parser = PermsParser(user=self.user, args=self.args).parse()
    #         if self.user in STREAM_GODS:
    #             return User(parser.target_user).paperup()

    #     # ---------------
    #     # Takes a Command
    #     # ---------------

    #     if self.command == "help":
    #         if len(self.args) > 0:
    #             command = self.args[0]
    #             if command.startswith("!"):
    #                 command = command[1:]
    #             return HELP_COMMANDS[command]
    #         else:
    #             options = " ".join([f"!{command}" for command in HELP_COMMANDS.keys()])
    #             return f"Call !help with a specfic command for more details: {options}"

    #     if self.command in ["dislike", "hate", "detract"]:
    #         parser = PermsParser(user=self.user, args=self.args).parse()

    #         if parser.target_command and not parser.target_user:
    #             result = SFXVote(parser.target_command).detract(self.user)
    #             return f"!{parser.target_command} supporters: {len(result['supporters'])} | detractors {len(result['detractors'])}"
    #         else:
    #             print("Doing Nothing")
    # def random_not_you_user(self):
    #     return find_random_user(blacklisted_users=[self.user])

    #     if self.command == "users":
    #         return WelcomeCommittee().present_users()
    #     if self.command == "richest":
    #         return " | ".join(
    #             [f"{stat[0]}: {stat[1]}" for stat in reversed(User.richest())]
    #         )
    #     if self.command == "facts" and self.user in STREAM_GODS:
    #         return Facts().available_sounds()
