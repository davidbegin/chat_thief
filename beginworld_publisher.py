from pathlib import Path
from shutil import copyfile, rmtree

import asyncio

import jinja2
from jinja2 import Template

from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.config.log import success, warning, error



rendered_template_path = Path(__file__).parent.joinpath("build/beginworld_finance")
template_path = Path(__file__).parent.joinpath("chat_thief/templates/")


def setup_build_dir():
    warning("Setting Up Build Dir")

    # Delete and Recreate Build Direction for BeginWorld Finance HTML
    rmtree(rendered_template_path, ignore_errors=True)
    # This aint working!!!
    rendered_template_path.mkdir(exist_ok=True, parents=True)

    # Move the CSS File
    css_source =  Path(__file__).parent.joinpath("chat_thief/static/style.css")
    css_dest = Path(__file__).parent.joinpath("build/beginworld_finance/style.css")
    copyfile(css_source, css_dest)


def _rendered_and_save_html(file_name, context):
    warning("Rendering Template")
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_path),
        # enable_async=True
    ).get_template(file_name)
    rendered_template = template.render(context)
    # await rendered_template = template.render_async(context)
    success("Finished Rendering Template")

    warning("Writing Template")
    with open(rendered_template_path.joinpath(file_name), "w") as f:
        f.write(rendered_template)
    success("Finished Writing Template")


def _rendered_and_save_html2(user, context):
    warning("Rendering Template")
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_path),
        # enable_async=True
    ).get_template("user.html")
    rendered_template = template.render(context)
    # await rendered_template = template.render_async(context)
    success("Finished Rendering Template")

    warning("Writing Template")
    with open(rendered_template_path.joinpath(f"{user}.html"), "w") as f:
        f.write(rendered_template)
    success("Finished Writing Template")

def generate_home():
    users = User.by_cool_points()
    commands = Command.by_cost()
    base_url = "/home/begin/code/chat_thief/build/beginworld_finance"
    context = {
        "users": users,
        "commands": commands,
        "base_url": base_url,
    }
    _rendered_and_save_html("beginworld_finance.html", context)


def generate_user_page(username):
    # rendered_template_path = Path(__file__).parent.joinpath("build/beginworld_finance")
    rendered_template_path.joinpath(username).mkdir(exist_ok=True)

    user = User(username)
    stats = user.stats()
    commands = user.commands()

    base_url = f"/home/begin/code/chat_thief/build/beginworld_finance/"

    context = {
        "user": user.name,
        "commands": commands,
        "stats": stats,
        "base_url": base_url,
    }

    _rendered_and_save_html2(user.name, context)


# async def generate_jinja_template():
#     t = Template("Hello {{ something }}!") 
#     t.render(something="World")
#     return t


if __name__ == "__main__":
    setup_build_dir()
    generate_home()

    for user in User.all():
        print(f"USER: {user}")
        generate_user_page(user)
