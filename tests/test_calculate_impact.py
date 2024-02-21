# questions only: 7311772
# wrong representation: 7367567 - 22814 vs 26k on site
from impact import StackExchangeImpact


class TestCalculateImpact:

    api = StackExchangeImpact(api=None)

    def test_01_empty(self):

        assert self.api._calculate_impact() == 0
