# questions only: 7311772
# wrong representation: 7367567 - 22814 vs 26k on site
from impact import StackExchangeImpact
import tests.data
import pytest


@pytest.fixture
def impact_no_api():
    return StackExchangeImpact(api=None)


class TestCalculateImpact:

    def test_01_empty(self, impact_no_api):

        assert impact_no_api._calculate_impact() == 0

    def test_02_asked_questions_only(self, impact_no_api):

        impact_no_api._questions_asked_views = tests.data.ASKED_QUESTIONS_10_1000

        assert impact_no_api._calculate_impact() == 10 * 1000

    def test_03_useful_answered_questions_only(self, impact_no_api):

        impact_no_api._answered_questions = tests.data.ANSWERED_QUESTIONS_10_1000_ALL_USEFUL

        assert impact_no_api._calculate_impact() == 10 * 1000

    def test_04_useless_answered_questions_only(self, impact_no_api):

        impact_no_api._answered_questions = tests.data.ANSWERED_QUESTIONS_10_1000_ALL_USELESS

        assert impact_no_api._calculate_impact() == 0

    def test_05_half_useful_answered_questions(self, impact_no_api):

        impact_no_api._answered_questions = tests.data.ANSWERED_QUESTIONS_20_1000_HALF_USEFUL

        assert impact_no_api._calculate_impact() == 10 * 1000

    def test_07_combined_answered_questions(self, impact_no_api):

        impact_no_api._questions_asked_views = tests.data.ASKED_QUESTIONS_10_1000
        impact_no_api._answered_questions = tests.data.ANSWERED_QUESTIONS_20_1000_HALF_USEFUL

        assert impact_no_api._calculate_impact() == 20 * 1000
