from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile, rmtree, copytree
import asyncio
import time
from datetime import datetime
import filecmp

import jinja2
from jinja2 import Template

from chat_thief.models.bot_vote import BotVote
from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.config.log import success, warning, error
from chat_thief.models.css_vote import CSSVote
from chat_thief.models.user_code import UserCode

from chat_thief.stitch_and_sort import StitchAndSort
from chat_thief.stats_department import StatsDepartment


rendered_template_path = Path(__file__).parent.parent.parent.joinpath(
    "build/beginworld_finance"
)
template_path = Path(__file__).parent.parent.joinpath("templates/")
base_url = "/home/begin/code/chat_thief/build/beginworld_finance"
DEPLOY_URL = "https://mygeoangelfirespace.city"


# this handles setup and destroy
def setup_build_dir():
    warning("Setting Up Build Dir")

    # Delete and Recreate Build Direction for BeginWorld Finance HTML
    old_build_path = Path(__file__).parent.parent.parent.joinpath(
        "tmp/old_build/beginworld_finance"
    )
    rmtree(old_build_path, ignore_errors=True)
    copytree(rendered_template_path, old_build_path)

    rmtree(rendered_template_path, ignore_errors=True)
    # This aint working!!!
    rendered_template_path.mkdir(exist_ok=True, parents=True)

    # Move the CSS File
    css_source = Path(__file__).parent.parent.joinpath("static")
    css_dest = Path(__file__).parent.parent.parent.joinpath(
        "build/beginworld_finance/styles"
    )
    copytree(css_source, css_dest)

    # Move JS Files
    js_source = Path(__file__).parent.parent.joinpath("js")

    js_dest = Path(__file__).parent.parent.parent.joinpath(
        "build/beginworld_finance/js"
    )
    copytree(js_source, js_dest)

    success("Finished Setting Up Build Dir")


async def _render_and_save_html(file_name, context, dest_filename=None):
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_path),
    ).get_template(file_name)

    rendered_template = template.render(context)

    if dest_filename:
        html_file = dest_filename
    else:
        html_file = file_name

    with open(rendered_template_path.joinpath(html_file), "w") as f:
        f.write(rendered_template)


async def generate_widgets_page(winner):
    widgets = UserCode.all()
    dev_leaderboard = UserCode.dev_leaderboard()

    context = {
        "base_url": DEPLOY_URL,
        "widgets": widgets,
        "winner": winner,
        "dev_leaderboard": dev_leaderboard,
    }
    await _render_and_save_html("widgets.html", context, "widgets.html")


async def generate_bots_page(winner):
    bots = User.bots()
    bot_votes = BotVote.count_by_group("bot")

    context = {
        "base_url": DEPLOY_URL,
        "bots": bots,
        "bot_votes": bot_votes,
        "winner": winner,
    }
    await _render_and_save_html("bots.html", context, "bots.html")


async def generate_stats_page(stats, winner):
    context = {
        "base_url": DEPLOY_URL,
        "winner": winner,
    }
    await _render_and_save_html("stats.html", {**context, **stats}, "stats.html")


async def generate_home(all_data, stylish_users, homepage_candidates, winner):
    # We just find fancy pages here
    commands = all_data["commands"]
    users = all_data["users"]

    updated_at = datetime.now().isoformat()

    new_styles = Path(__file__).parent.parent.joinpath("static/")
    old_styles = Path(__file__).parent.parent.parent.joinpath(
        "tmp/old_build/beginworld_finance/styles/"
    )

    recently_updated_users = [
        f.split(".")[0] for f in filecmp.dircmp(new_styles, old_styles).diff_files
    ]
    context = {
        "recently_updated_users": recently_updated_users,
        "candidates": homepage_candidates,
        "updated_at": updated_at,
        "winner": winner,
        "users": users,
        "stylish_users": sorted(stylish_users),
        "commands": commands,
        "base_url": DEPLOY_URL,
    }
    await _render_and_save_html("beginworld_finance.html", context, "index.html")


async def generate_command_page(cmd_dict, winner):
    name = cmd_dict["name"]
    Path(base_url).joinpath("commands").mkdir(exist_ok=True)

    if len(cmd_dict["permitted_users"]) > -1:
        context = {
            "winner": winner,
            "name": cmd_dict["name"],
            "command_file": cmd_dict.get("command_file", None),
            "users": cmd_dict["permitted_users"],
            "cost": cmd_dict["cost"],
            "like_to_hate_ratio": cmd_dict["like_to_hate_ratio"],
            "base_url": DEPLOY_URL,
        }

        await _render_and_save_html(
            "command.html", context, f"commands/{cmd_dict['name']}.html"
        )


# We could add some logic here so it shows your a stream god
async def generate_user_page(user_dict, all_commands):
    name = user_dict["name"]
    if name in STREAM_GODS:
        commands = all_commands
    else:
        commands = user_dict["commands"]

    commands = list(
        reversed(sorted(commands, key=lambda command: command.get("cost", 0)))
    )

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

    # if approved_widgets or deactivated_widgets:
    #     print(f"Approved Widgets: {approved_widgets}")
    #     print(f"Deactivated Widets: {deactivated_widgets}")

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


# cyberbeni: Isn't asyncio single threaded? I think you need a
# ProcessPoolExecutor or a ThreadPoolExecutor to speed it up.
async def main():
    warning("Fetching All Data")
    all_data = StitchAndSort().call()
    stats = StatsDepartment().stats()
    success("All Data Fetched...Creating Tasks")
    all_commands = [command["name"] for command in all_data["commands"]]

    static_dir = Path(__file__).parent.parent.joinpath("static")
    stylish_users = [f.name[: -len(f.suffix)] for f in static_dir.glob("*.css")]

    print(f"Stylish Users: {stylish_users}")

    homepage_candidates = CSSVote.by_votes()
    try:
        winner = homepage_candidates[0][0]
    except:
        winner = User.wealthiest()

    warning("Setting Up Tasks")
    tasks = (
        [generate_home(all_data, stylish_users, homepage_candidates, winner)]
        + [generate_bots_page(winner)]
        + [generate_widgets_page(winner)]
        + [generate_stats_page(stats, winner)]
        + [
            generate_user_page(user_dict, all_commands)
            for user_dict in all_data["users"]
        ]
        + [generate_command_page(command, winner) for command in all_data["commands"]]
    )
    success("Finished Setting Up Tasks")

    await asyncio.gather(*[asyncio.create_task(task) for task in tasks])


if __name__ == "__main__":
    setup_build_dir()
    asyncio.run(main())
