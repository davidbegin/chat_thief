from tinydb import Query

from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.command import Command


@object.__new__
class TheFed(BaseDbModel):
    table_name = "the_fed"
    database_path = "db/the_fed.json"
    version = "0.0.0"

    @classmethod
    def reserve(cls):
        if command := cls.db().get(Query().version == cls.version):
            return command["reserve"]
        else:
            return 0

    def collect_taxes(self):
        for command in Command.db().all():
            if command["cost"] > 1:
                print(f"Taxing {command['name']}")
                new_cost = int(command["cost"] / 2)
                Command(command["name"]).set_value("cost", new_cost)
                self.collect_tax(new_cost)

    def collect_tax(self, tax):
        if self.db().search(Query().version == self.version):
            self._update_value("reserve", tax)
        else:
            self._reserve = tax
            self.save()

    def pay(self, tax):
        self._update_value("reserve", -tax)

    def _update_value(self, field, amount=1):
        def _update_that_value():
            def transform(doc):
                doc[field] = doc[field] + amount

            return transform

        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.update_callable(_update_that_value(), Query().version == self.version)

    def doc(self):
        return {"version": self.version, "reserve": self._reserve}
