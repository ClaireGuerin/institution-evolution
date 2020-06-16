import pytest
from institutionevolution.individual import Individual as Ind

class TestDebateFeature(object):

	def test_individuals_invest_time_into_debate(self):
		self.ind = Ind()
		assert hasattr(self.ind, "debateTime"), "the individual does not have time for debate"
