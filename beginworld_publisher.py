from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile, rmtree

import asyncio

import jinja2
from jinja2 import Template

from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.config.log import success, warning, error


rendered_template_path = Path(__file__).parent.joinpath("build/beginworld_finance")
template_path = Path(__file__).parent.joinpath("chat_thief/templates/")
base_url = "/home/begin/code/chat_thief/build/beginworld_finance"
deploy_url = "http://beginworld.exchange-f27cf15.s3-website-us-west-2.amazonaws.com"


# this handles setup and destroy
def setup_build_dir():
    warning("Setting Up Build Dir")

    # Delete and Recreate Build Direction for BeginWorld Finance HTML
    rmtree(rendered_template_path, ignore_errors=True)
    # This aint working!!!
    rendered_template_path.mkdir(exist_ok=True, parents=True)

    # Move the CSS File
    css_source = Path(__file__).parent.joinpath("chat_thief/static/style.css")
    css_dest = Path(__file__).parent.joinpath("build/beginworld_finance/style.css")
    copyfile(css_source, css_dest)


def _render_and_save_html(file_name, context, dest_filename=None):
    warning("Rendering Template")
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_path),
        # enable_async=True
    ).get_template(file_name)

    rendered_template = template.render(context)
    # await rendered_template = template.render_async(context)
    success("Finished Rendering Template")

    warning("Writing Template")
    if dest_filename:
        html_file = dest_filename
    else:
        html_file = file_name

    with open(rendered_template_path.joinpath(html_file), "w") as f:
        f.write(rendered_template)
    success("Finished Writing Template")


def generate_home():
    users = User.by_cool_points()
    commands = Command.by_cost()
    context = {
        "users": users,
        "commands": commands,
        "base_url": deploy_url,
    }
    _render_and_save_html("beginworld_finance.html", context, "index.html")


def generate_command_page(command):
    Path(base_url).joinpath("commands").mkdir(exist_ok=True)

    command_name = command["name"]
    command = Command(command_name)

    if len(command.users()) > -1:
        # if len(command.users()) > 0:
        print(f"Command: {command_name}")
        sfx_vote = SFXVote(command_name)

        context = {
            "name": command_name,
            "users": command.users(),
            "cost": command.cost,
            "like_to_hate_ratio": sfx_vote.like_to_hate_ratio(),
            "base_url": deploy_url,
        }

        _render_and_save_html("command.html", context, f"commands/{command_name}.html")


def generate_user_page(username):
    user = User(username)
    stats = user.stats()
    commands = user.commands()

    context = {
        "user": user.name,
        "commands": commands,
        "stats": stats,
        "base_url": deploy_url,
    }

    _render_and_save_html("user.html", context, f"{user.name}.html")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--users", "-u", action="store_true", dest="generate_users", default=False
    )
    parser.add_argument(
        "--commands", "-c", action="store_true", dest="generate_commands", default=False
    )
    args = parser.parse_args()
    # parser.add_argument("--user", "-u", dest="user", default="beginbotbot")
    # parser.add_argument(
    #     "--breakpoint", "-b", dest="breakpoint", action="store_true", default=False
    # )
    # setup_build_dir()
    # generate_home()

    if args.generate_users:
        for user in User.all():
            print(f"USER: {user}")
            generate_user_page(user)

    # A bunch of commands are theme songs
    # we want to filter out theme_songs
    if args.generate_commands:
        for command in Command.all():
            generate_command_page(command)
