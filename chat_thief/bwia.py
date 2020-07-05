import itertools
import operator

from tinydb import Query  # type: ignore

from chat_thief.models.user_event import UserEvent


class BWIA:
    @classmethod
    def robinhood_score(cls, user):
        return len(
            UserEvent.db().search(
                ((Query().command == "give") | (Query().command == "share"))
                & (Query().user == user)
            )
        )

    @classmethod
    def find_thief(cls, thief):
        return len(
            UserEvent.db().search(
                (Query().command == "steal") & (Query().user == thief)
            )
        )

    @classmethod
    def thieves(cls):
        steal_events = UserEvent.db().search(Query().command == "steal")
        thieves = itertools.groupby(steal_events, operator.itemgetter("user"))

        steal_counts = []
        for thief, user_events in thieves:
            steal_count = 0
            for event in user_events:
                steal_count += 1
            steal_counts.append((thief, steal_count))

        return steal_counts
