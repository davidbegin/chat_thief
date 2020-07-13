from argparse import ArgumentParser
from pathlib import Path
import asyncio
import time
from datetime import datetime

import jinja2
from jinja2 import Template

from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.config.log import success, warning, error
from chat_thief.models.css_vote import CSSVote
from chat_thief.models.user_code import UserCode

from chat_thief.stitch_and_sort import StitchAndSort
from chat_thief.stats_department import StatsDepartment
from chat_thief.mygeoangelfirespace.publisher import setup_build_dir, _render_and_save_html


base_url = "/home/begin/code/chat_thief/build/beginworld_finance"
DEPLOY_URL = "https://mygeoangelfirespace.city"


# We could add some logic here so it shows your a stream god
async def generate_user_page(user_dict, all_commands):
    name = user_dict["name"]
    if name in STREAM_GODS:
        commands = all_commands
    else:
        commands = User(name).commands()

    # commands = list(
    #     reversed(sorted(commands, key=lambda command: command.get("cost", 0)))
    # )

    users_choice = user_dict.get("custom_css", None)
    ride_or_die = user_dict.get("ride_or_die", None)

    stats = (
        f"@{name} - Mana: {user_dict['mana']} | "
        f"Street Cred: {user_dict['street_cred']} | "
        f"Cool Points: {user_dict['cool_points']}"
    )

    if wealth := user_dict.get("wealth", None):
        stats += f" | Wealth: {user_dict['wealth']}"

    top8 = user_dict.get("top_eight", [])

    widgets = user_dict.get(
        "widgets", {"approved": [], "unapproved": [], "deactivated": []}
    )
    deactivated_widgets = widgets.get("deactivated", [])
    approved_widgets = [
        widget
        for widget in widgets["approved"]
        if widget.lower() not in deactivated_widgets
    ]

    context = {
        "user": name,
        "command_file": user_dict.get("command_file", None),
        "users_choice": users_choice,
        "commands": commands,
        "stats": stats,
        "top8": top8,
        "base_url": DEPLOY_URL,
        "widgets": approved_widgets,
        "unapproved_widgets": widgets["unapproved"],
        "deactivated_widgets": deactivated_widgets,
    }
    await _render_and_save_html("user.html", context, f"{name}.html")


async def main(user):
    print(f"Generating Home Page for: {user}")
    all_commands = [ command for command in Command.all() ]
    user_dict = User(user)._find_or_create_user()
    tasks = [ generate_user_page(user_dict, all_commands) ]
    await asyncio.gather(*[ asyncio.create_task(task) for task in tasks ])


if __name__ == "__main__":
    setup_build_dir()
    parser = ArgumentParser()
    parser.add_argument("--user", "-u", dest="user", default="beginbotbot")
    args = parser.parse_args()
    asyncio.run(main(args.user))
