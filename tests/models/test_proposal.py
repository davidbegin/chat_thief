import pytest

from chat_thief.models.proposal import Proposal

from tests.support.database_setup import DatabaseConfig


class TestProposal(DatabaseConfig):
    def test_it_is_real(self):
        assert Proposal.count() == 0
        Proposal(user="bobby", command="iasip", proposal="The Gang Steals Kappa").save()
        assert Proposal.count() == 1

    def test_find_by_user(self):
        Proposal(user="bobby", command="iasip", proposal="The Gang Steals Kappa").save()
        proposal = Proposal.find_by_user("bobby")
        assert proposal["proposal"] == "The Gang Steals Kappa"

    def test_support(test):
        Proposal(user="bobby", command="iasip", proposal="The Gang Steals Kappa").save()
        proposal = Proposal.last()
        Proposal.support("bobby", proposal.doc_id, "sumo")
        assert Proposal.find_by_user("bobby")["supporters"] == ["sumo"]
