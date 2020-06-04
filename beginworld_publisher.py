from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile, rmtree, copytree
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
    old_build_path = Path(__file__).parent.parent.joinpath(
        "tmp/old_build/beginworld_finance"
    )
    rmtree(old_build_path, ignore_errors=True)
    copytree(rendered_template_path, old_build_path)

    rmtree(rendered_template_path, ignore_errors=True)
    # This aint working!!!
    rendered_template_path.mkdir(exist_ok=True, parents=True)

    # Move the CSS File
    css_source = Path(__file__).parent.joinpath("chat_thief/static/baldclap.css")
    css_dest = Path(__file__).parent.joinpath("build/beginworld_finance/style.css")
    copyfile(css_source, css_dest)
    success("Finished Setting Up Build Dir")


async def _render_and_save_html(file_name, context, dest_filename=None):
    warning(f"Rendering Template: {dest_filename}")
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_path),
        # enable_async=True
    ).get_template(file_name)

    rendered_template = template.render(context)
    success(f"Finished Rendering Template: {dest_filename}")

    warning(f"Writing Template: {file_name}")
    if dest_filename:
        html_file = dest_filename
    else:
        html_file = file_name

    with open(rendered_template_path.joinpath(html_file), "w") as f:
        f.write(rendered_template)
    success(f"Finished Writing Template: {file_name}")


async def generate_home():
    commands = Command.by_cost()
    users = User.by_cool_points()
    context = {
        "users": users,
        "commands": commands,
        "base_url": deploy_url,
    }
    await _render_and_save_html("beginworld_finance.html", context, "index.html")


async def generate_command_page(cmd_dict):
    name = cmd_dict["name"]
    Path(base_url).joinpath("commands").mkdir(exist_ok=True)

    if len(cmd_dict["permitted_users"]) > -1:
        context = {
            "name": cmd_dict["name"],
            "users": cmd_dict["permitted_users"],
            "cost": cmd_dict["cost"],
            "like_to_hate_ratio": cmd_dict["like_to_hate_ratio"],
            "base_url": deploy_url,
        }

        await _render_and_save_html(
            "command.html", context, f"commands/{cmd_dict['name']}.html"
        )


# We need to fetch all the info upfront
# Fetching the info from the DB is blocking!
async def generate_user_page(user_dict):
    name = user_dict["name"]
    commands = user_dict["commands"]
    stats = f"@{name} - Mana: {user_dict['mana']} | Street Cred: {user_dict['street_cred']} | Cool Points: {user_dict['cool_points']}"

    context = {
        "user": name,
        "commands": commands,
        "stats": stats,
        "base_url": deploy_url,
    }

    await _render_and_save_html("user.html", context, f"{name}.html")


# cyberbeni: Isn't asyncio single threaded? I think you need a
# ProcessPoolExecutor or a ThreadPoolExecutor to speed it up.
async def main():
    warning("Fetching Users")
    users = User.all_data()
    success("Finished Fetching Users")

    warning("Fetching Commands")
    commands = Command.all_data()
    success("Finished Fetching Commands")

    warning("Setting Up Tasks")
    tasks = (
        [generate_home()]
        + [generate_user_page(user_dict) for user_dict in users]
        + [generate_command_page(command) for command in commands]
    )
    success("Finished Setting Up Tasks")

    await asyncio.gather(*[asyncio.create_task(task) for task in tasks])


if __name__ == "__main__":
    setup_build_dir()
    asyncio.run(main())
