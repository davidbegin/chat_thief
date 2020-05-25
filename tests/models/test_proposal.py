import time
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

    def test_cannot_support_yourself(self):
        Proposal(user="bobby", command="iasip", proposal="The Gang Steals Kappa").save()
        proposal = Proposal.last()
        result = Proposal.support("bobby", proposal.doc_id, "bobby")
        assert result == "Can't support yourself @bobby"
        assert Proposal.find_by_user("bobby")["supporters"] == []

    def test_no_double_support(self):
        Proposal(user="bobby", command="iasip", proposal="The Gang Steals Kappa").save()
        proposal = Proposal.last()
        result = Proposal.support("bobby", proposal.doc_id, "sumo")
        assert Proposal.find_by_user("bobby")["supporters"] == ["sumo"]
        assert result == "@bobby Thanks You for the support @sumo"
        result = Proposal.support("bobby", proposal.doc_id, "sumo")
        assert Proposal.find_by_user("bobby")["supporters"] == ["sumo"]
        assert result == "You already supported! @sumo"

    def test_support_last(test):
        Proposal(user="bobby", command="iasip", proposal="The Gang Steals Kappa").save()
        Proposal.support_last("sumo")
        assert Proposal.find_by_user("bobby")["supporters"] == ["sumo"]

    def test_proposals_expire(self):
        proposal = Proposal(
            user="bobby", command="iasip", proposal="The Gang Steals Kappa"
        ).save()
        OG_PROPOSAL_TIME = Proposal.EXPIRE_TIME_IN_SECS
        assert not proposal.is_expired()
        Proposal.EXPIRE_TIME_IN_SECS = 0
        assert proposal.is_expired()
        Proposal.EXPIRE_TIME_IN_SECS = OG_PROPOSAL_TIME
