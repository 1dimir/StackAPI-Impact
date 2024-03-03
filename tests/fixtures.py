import pytest
import unittest.mock as mock
import stackapi
import impact
import tests.data as sample


@pytest.fixture
def impact_no_api():
    """Returns an instance of StackExchangeImpact class with a dummy api attribute"""
    return impact.StackExchangeImpact(api=1)


@pytest.fixture
def api() -> mock.Mock:
    """Returns mocked instance of stackapi.StackAPI class with some constants set-up"""
    api_factory = mock.Mock(stackapi.StackAPI, autospec=True)
    api = api_factory.return_value
    api.page_size = sample.PAGE_SIZE

    return api


@pytest.fixture
def regular_answered_question():
    """Returns an instance of answered.Question with initialized question_id and small positive answer score"""
    return sample.question(
        question_id=1,
        score=1,
        is_accepted=False)


@pytest.fixture
def accepted_answered_question():
    """Returns an instance of answered.Question and `is_accepted` set to True"""
    return sample.question(
        question_id=1,
        score=1,
        is_accepted=True)


@pytest.fixture
def answered_question_dont_inspect():
    """Returns an instance of answered.Question which is accepted and doesn't require inspection of all answers"""
    return sample.question(
        question_id=1,
        score=1,
        is_accepted=True,
        inspect_answers=False,
        answer_count=10,
        useful=True)


@pytest.fixture
def answered_question_require_inspection():
    """Returns an instance of answered.Question which isn't accepted and requires inspection of all answers"""
    return sample.question(
        question_id=1,
        score=1,
        is_accepted=False,
        inspect_answers=True,
        answer_count=10,
        useful=False)
