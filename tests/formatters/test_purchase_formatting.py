import pytest

from chat_thief.formatters.purchase_formatter import PurchaseFormatter
from chat_thief.new_commands.result import Result

from tests.support.database_setup import DatabaseConfig


class TestPurchaseFormatter(DatabaseConfig):
    def test_format_successful_purchase(self):
        result = Result(user="uzi", command="handbag", metadata={})
        assert PurchaseFormatter(result).format()
