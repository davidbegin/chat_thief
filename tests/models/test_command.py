from pathlib import Path

import pytest

from chat_thief.models.command import Command
from chat_thief.models.user import User
from chat_thief.models.sfx_vote import SFXVote

from tests.support.database_setup import DatabaseConfig


class TestCommand(DatabaseConfig):
    def test_count(self):
        assert Command.count() == 0

    def test_allowed_to_play(self):
        subject = Command("help")
        assert subject.allowed_to_play("beginbotbot")

    def test_not_allowed_to_play_others_themes(self):
        subject = Command("artmattdank")
        assert subject.allowed_to_play("artmattdank")
        assert not subject.allowed_to_play("beginbot")

    def test_allow_user(self):
        subject = Command("clap")
        other_subject = Command("damn")
        assert not subject.allowed_to_play("spfar")
        assert not subject.allowed_to_play("rando")
        assert not other_subject.allowed_to_play("spfar")
        assert not other_subject.allowed_to_play("rando")
        subject.allow_user("spfar")
        other_subject.allow_user("rando")
        assert subject.allowed_to_play("spfar")
        assert not subject.allowed_to_play("rando")
        assert not other_subject.allowed_to_play("spfar")
        assert other_subject.allowed_to_play("rando")
        subject.allow_user("rando")
        assert subject.allowed_to_play("rando")

    def test_unallow(self):
        subject = Command("clap")
        other_subject = Command("damn")
        subject.allow_user("spfar")
        other_subject.allow_user("rando")

        assert subject.allowed_to_play("spfar")
        subject.unallow_user("spfar")
        assert not subject.allowed_to_play("spfar")

    def test_cost(self):
        subject = Command("clap")
        subject.save()
        assert subject.cost() == 1
        subject.increase_cost()
        assert subject.cost() == 2

    def test_find_or_create(self):
        assert Command.count() == 0
        command = Command.find_or_create("clap")
        assert Command.count() == 1
        command = Command.find_or_create("clap")
        assert Command.count() == 1

    def test_silence_and_revive(self):
        subject = Command("damn")
        subject.save()
        assert subject.health() == 3
        subject.silence()
        assert subject.health() == 0
        subject.revive()
        assert subject.health() == 3

    def test_most_expensive_command(self):
        assert not Command.most_expensive()
        damn_cmd = Command("damn")
        damn_cmd.save()

        chain_cmd = Command("mchdtmd")
        chain_cmd.save()
        chain_cmd.increase_cost(20)

        win_cmd = Command("win")
        win_cmd.save()
        win_cmd.increase_cost(10)
        assert Command.most_expensive()["name"] == "mchdtmd"

    def test_decay(self):
        command = Command("damn", 10)
        command.save()
        command.decay()
        assert command.cost() == 9

        command = Command("handbag")
        command.save()
        command.decay()
        assert command.cost() == 1
