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
            if command['cost'] > 1:
                print(f"Taxing {command['name']}")
                new_cost =  int(command['cost'] / 2)
                Command(command['name']).set_value("cost", new_cost)
                self.collect_tax(new_cost)


    def collect_tax(self, tax):
        self._reserve =  tax
        self.save()

    def doc(self):
        return {
            "version": self.version,
            "reserve": self._reserve
        }
