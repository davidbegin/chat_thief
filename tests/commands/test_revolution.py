import pytest

from chat_thief.commands.revolution import Revolution


# We hide the Cost
class TestRevolution:

    # Coup costs something, it doubles everytime
    # If you don't have the costs, you lose all you currency
    def test_attempt_coup(self):
        assert True
