import pytest
from impact import StackExchangeImpact
from tests.data import question


@pytest.fixture
def impact_no_api():
    return StackExchangeImpact(api=None)


@pytest.fixture
def regular_answered_question():
    return question(
        question_id=1,
        score=1,
        is_accepted=False)


@pytest.fixture
def accepted_answered_question():
    return question(
        question_id=1,
        score=1,
        is_accepted=True)
