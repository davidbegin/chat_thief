import pytest
from pathlib import Path

from chat_thief.models.notification import Notification
from chat_thief.audioworld.audio_player import AudioPlayer
from tests.support.database_setup import DatabaseConfig


class TestAudioPlayer(DatabaseConfig):
    def test_notifications(self):
        fake_sound = Path(__file__)
        assert Notification.count() == 0
        AudioPlayer.play_sample(fake_sound)
        assert Notification.count() == 1

    def test_no_notification(self):
        fake_sound = Path(__file__)
        assert Notification.count() == 0
        AudioPlayer.play_sample(fake_sound, notification=False)
        assert Notification.count() == 0
