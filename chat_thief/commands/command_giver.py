from chat_thief.models.user import Command


class CommandGiver:
    def __init__(self, user, command, friend):
        self.user = user
        self.command = command
        self.friend = friend

    def give(self):
        permitted_users = Command(name=self.command).users()

        if self.user in STREAM_GODS:
            return f"YOU'RE A STREAM GOD @{self.user} YOU DON'T NEED TO SWAP PERMS"
        else:
            print(f"Permitted Users For: !{self.command} {permitted_users}")
            if self.user in permitted_users:
                allow_msg = self.command.allow_user(self.friend)
                return [allow_msg, self.command.unallow_user(self.user)]
            else:
                return f"@{self.user} does not have permission to give: {self.command}"

    def swap_perm(self):
        print(f"Transferring !{self.command} from @{self.user} to @{self.friend}")
        command = Command(self.command)
        allow_result = command.allow_user(self.friend)
        unallow_result = command.unallow_user(self.user)
        return allow_result + " " + unallow_result
